import datetime
import re

import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseDetoSpider(BaseGazetteSpider):
    """
    Este site é bastante complicado de interagir de forma programática porque ele utiliza de conteúdo dinâmico e AJAX
    para manipular os elementos da tela e permitir o usuário baixar os diários.
    A lógica descrita aqui foi entendida a partir de engenharia reversa das diferentes requisições feitas por funções JS.
    O que descobri sobre o funcionamento do site:
    - Ele começa exibindo uma tabela paginada de dias com diário oficial, cada um com um botão para uma função JS
    que requisita dados do backend
    - Ao clicar no botão, um modal com os diários daquele dia aparece, com um botão para outra função JS
    - Ao clicar neste, uma requisição é finalmente feita para baixar o PDF
    - As paginações são feitas através da substituição de html retornadas das requisições AJAX ao backend
    - As requisições relevantes para raspagem são feitas para diferentes endpoints, sob diferentes métodos
      - Os POSTs tem parâmetros no body. Os GETs tem parâmetros no hash
      - Umas retornam HTML, e outros, um JSON com diversos itens, que assumo servirem para gerenciar o estado do JS.
        - No JSON, HTML é retornado no array 'setValue'. Este tem itens com 'field' e 'value'. O item com
        'field' == 'sc_grid_body' tem a string HTML que será substituída no DOM como 'value'.
      - O tipo do retorno de cada endpoint muda de acordo com parâmetros e eu não investiguei todas as possibilidades.
        - As relevantes são listadas abaixo
      - 'opc' e 'parm' são os dois parâmetros principais. Seus valores definem o que será retornado pelo backend:
        - opc=muda_qt_linhas, parm=11
          - retorna HTML
          - atualiza o tamanho da página para 11 itens e retorna a página atual com esta quantidade
          - pode configurar uma quantidade acima do máximo descrito na UI
        - opc=muda_rec_linhas, parm=11
          - carrega uma página de itens a partir do 11º item,
          - retorna JSON se o Content-Type for application/x-www-form-urlencoded
            - Senão, HTML é retornado mas não obedece a paginação e sempre retorna a primeira página
        - opc=rec, parm=11
          - igual à 'muda_rec_linhas'
    """

    page_size = 10
    custom_settings = {"DOWNLOAD_DELAY": 1.0}
    pages_consumed = 0
    total_pages_count = None
    script_case_session = None

    def start_requests(self):
        data = {
            "nmgp_parms": "nm_run_menu?#?1?@?nm_apl_menu?#?menu_diarioeletronico?@?script_case_init?#?1",
            "script_case_init": "1",
            "nm_apl_menu": "menu_diarioeletronico",
        }

        yield FormRequest(
            url=f"{self.BASE_URL}/diarioeletronico_grid_cliente/",
            formdata=data,
            callback=self.parse_table,
        )

    def parse_table(self, response, has_json_response=False):
        """
        Interpreta uma tabela (página) de diários oficiais, contendo <tam. de página> linhas com links para abertura
        de um modal.
        Consome seu conteúdo gerando uma requisição para cada item, mais outra requisição para a próxima página,
        se existir.
        'has_json_response' indica o retorno esperado da requisição (html ou json), sendo que ela muda conforme
        o endpoint usado. O content-type retornado pelo backend não pode ser confiado.
        """

        # O rodapé pego aqui só está disponível na primeira requisição de tabela, que retorna html.
        # As requisições para as próximas paginas retornam json, com html dentro, e este não tem o rodapé.
        # Calculamos a quantidade total de itens e páginas para poder gerenciar o consumo das páginas nós mesmos
        if self.total_pages_count is None:
            self.total_pages_count = self.extract_total_items_count(response)

        # Este valor é usado em requisições seguintes. Pegamos ele aqui na primeira requisição
        # if self.script_case_session is None:
        #     self.script_case_session = response.xpath(
        #         '//form[@name="form_ajax_redir_1"]//input[@name="script_case_session"]/@value'
        #     ).get()

        # Em algumas chamadas (todas além da primeira), o response é um JSON
        # Então, normalizo o objeto response para que se comporte como se este fosse um response derivado de html,
        # ou seja, response.xpath, etc, estão disponíveis
        if has_json_response:
            # Encontra o html que está perdido dentro do JSON.
            # Está dentro do array setValue. O item com field == sc_grid_body tem como value o html
            html_text = next(
                (
                    item["value"]
                    for item in response.json()["setValue"]
                    if item["field"] == "sc_grid_body"
                ),
                None,
            )
            response = Selector(text=html_text)

        yield from self.consume_table_items(response)

        yield from self.maybe_request_next_page()

    def consume_table_items(self, response):
        """
        Chamado pelo parse_table para identificar todos os links da tabela e gerar uma requisição para cada.
        A requisição na UI abre um modal com links para os documentos.
        """
        self.pages_consumed = self.pages_consumed + 1

        # Cada linha tem um link cujo href contem parâmetros para abrir o modal
        lines = response.xpath('//tr[starts-with(@id, "SC_ancor")]').getall()

        for line in lines:
            # O href é uma chamada dum método JS. Precisamos do terceiro parâmetro para passar na próxima requisição.
            # Este parâmetro tem um sufixo hexadecimal
            modal_params = self.extract_modal_params(line)

            if modal_params is None:
                continue

            # Extrai a data da edição
            date_str = (
                Selector(text=line)
                .xpath('//span[starts-with(@id, "id_sc_field_dataedicao_")]/text()')
                .get()
            )
            doc_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()

            # Extrai o número da edição
            doc_edition = (
                Selector(text=line)
                .xpath('//span[starts-with(@id, "id_sc_field_numeroedicao_")]/text()')
                .get()
            )

            # Data e número da edição são enviados para o callback
            item_params = {
                "doc_date": doc_date,
                "doc_edition": doc_edition,
            }

            modal_url = (
                f"{self.BASE_URL}/diarioeletronico_form_cliente/?"
                # f"script_case_session={self.script_case_session}&"
                f"nmgp_outra_jan=true&"
                f"nmgp_url_saida=modal&"
                f"SC_lig_apl_orig=diarioeletronico_grid_cliente&"
                f"nmgp_parms={modal_params}"
            )

            yield scrapy.Request(
                url=modal_url,
                callback=self.parse_modal_items,
                cb_kwargs=item_params,
            )

    def maybe_request_next_page(self):
        """
        Chamado pelo parse_table para identificar se existem mais páginas a serem consumidas, gerando uma requisição
        para obter a próxima tabela caso exista.
        O Content-Type: application/x-www-form-urlencoded faz o resultado ser um JSON em vez de HTML.
        Parece que o backend tem um bug que faz o resultado HTML sempre retornar os dados da primeira página.
        """
        has_next_page = False

        if self.pages_consumed <= self.total_pages_count:
            has_next_page = True

        if self.pages_consumed >= 5:
            has_next_page = False

        if has_next_page:
            next_page_start = self.pages_consumed * self.page_size + 1

            data = {
                "nmgp_opcao": "ajax_navigate",
                "script_case_init": "1",
                "opc": "rec",
                "parm": str(next_page_start),
            }

            yield FormRequest(
                url=f"{self.BASE_URL}/diarioeletronico_grid_cliente/",
                formdata=data,
                callback=self.parse_table,
                cb_kwargs={"has_json_response": True},
            )

    def parse_modal_items(self, response, doc_date, doc_edition):
        """
        Interpreta um modal que exibe links para os documentos daquele dia.
        Terá mais de um no caso de edições extras.
        Gera um Gazette para cada item presente.
        doc_date é a data associada
        doc_edition é o número da edição
        """

        # A requisição pode ser inválida apesar de retornar 200 OK
        if "Dados inválidos" in response.text:
            self.logger.error(
                f"'Dados Inválidos' na resposta da requisição para modal da edição {doc_edition}. URL {response.request.url}"
            )
            self.logger.error("Abortando.")
            return

        # Extrai o href do link dentro do <div id="id_sc_loaded_anexo">
        script_case_init = response.xpath(
            '//form[@name="F1"]//input[@name="script_case_init"]/@value'
        ).get()

        doc_href = response.xpath('//div[@id="id_sc_loaded_anexo"]//a/@href').get()

        # Este href também é uma chamada JS.
        # O segundo parâmetro tem o nome do arquivo que será usado na requisição
        doc_name = None
        if doc_href:
            match = re.search(r"'documento_db', '(.+?)'", doc_href)
            if match:
                doc_name = match.group(1)

        is_extra_edition = False

        gazette_url = (
            f"{self.BASE_URL}/diarioeletronico_form_cliente/diarioeletronico_form_cliente_doc.php?"
            f"script_case_init={script_case_init}"
            f"&nm_cod_doc=documento_db"
            f"&nm_nome_doc={doc_name}"
            f"&nm_cod_apl=diarioeletronico_form_cliente"
        )

        yield Gazette(
            date=doc_date,
            edition_number=doc_edition,
            is_extra_edition=is_extra_edition,
            file_urls=[gazette_url],
            power="executive",
        )
