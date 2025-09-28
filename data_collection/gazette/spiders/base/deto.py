import datetime
import math
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
        'field' == 'sc_grid_body' tem a string HTML, que será substituída no DOM.
      - O tipo do retorno de cada endpoint muda de acordo com parâmetros e eu não investiguei todas as possibilidades.
        - As relevantes são listadas abaixo
      - 'opc' e 'parm' são os dois parâmetros principais. Seus valores definem o que será retornado pelo backend:
        - opc=muda_qt_linhas, parm=11
          - retorna HTML
          - atualiza o tamanho da página para 11 itens e retorna a página atual com esta quantidade
        - opc=muda_rec_linhas, parm=11
          - carrega uma página de itens a partir do 11º item,
          - retorna JSON se o Content-Type for application/x-www-form-urlencoded
            - Senão, HTML é retornado mas não obedece a paginação e sempre retorna a primeira página
        - opc=rec, parm=11
          - igual à 'muda_rec_linhas'

    Em resumo, o fluxo aqui acontece assim:
    1. Um POST é feito para `diarioeletronico_grid_cliente` para obter HTML com uma tabela de links para cada dia
    2. O resultado é enviado para `parse_table`, que chama dois métodos para consumir a tabela e a próxima página
    3. `consume_table_items` é chamado com os itens da tabela para consumí-los, e `maybe_request_next_page` é chamado
    para decidir se uma próxima página deve ser obtida
    4. `consume_table_items` extrai links de cada linha e faz um GET para `diarioeletronico_form_cliente` para obter
    a lista de diários daquele dia
    5. O resultado é enviado para `parse_modal_items`. "modal" porque o link abre um modal na UI
    6. `parse_modal_items` extrai os links para `diarioeletronico_form_cliente_doc` da lista de diários do dia e
    cria um Gazette para cada
    7. `maybe_request_next_page` decide se a próxima página deve ser requisitada baseado na quantidade de
    páginas/itens consumidos
    8. Caso positivo, um POST é feito para `diarioeletronico_grid_cliente` e o resultado vai para `parse_table`,
    reiniciando o ciclo no item 2

    Além destes pontos, o backend se comporta mal quando múltiplas requisições são feitas em paralelo, ou se estas
    ocorrerem fora da ordem esperada.
    A ordem esperada seria requisitar links de uma página antes de mudar para a próxima página.
    Quando estas premissas não são mantidas, o backend reponde requisições para obter o DOEM com um html
    dizendo 'Dados Inválidos'.
    Sendo assim, configurações do Scrapy personalizadas são feitas aqui para garantir que apenas uma requisição
    aconteça por vez, e as requisições para obter documentos tenham prioridade sempre maior que aquelas para
    obter próximas páginas.
    """

    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "CONCURRENT_REQUESTS_PER_IP": 1,
        "AUTOTHROTTLE_ENABLED": False,
    }
    page_size = 10
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

    def parse_table(self, response, has_json_response=False, pages_consumed=0):
        """
        Interpreta uma tabela (página) de diários oficiais, contendo <tam. de página> linhas com links para abertura
        de um modal.
        Consome seu conteúdo gerando uma requisição para cada item, mais outra requisição para a próxima página,
        se existir.
        'has_json_response' indica o retorno esperado da requisição (html ou json), sendo que ela muda conforme
        o endpoint usado. O content-type retornado pelo backend não pode ser confiado.
        'pages_consumed' conta a quantidade de páginas consumidas, lidas por este método.
        """

        # O rodapé é lido aqui somente uma vez para pegar a quantidade total de itens.
        # Calculamos a quantidade total de itens e páginas para poder gerenciar o consumo das páginas nós mesmos
        if self.total_pages_count is None:
            self.total_pages_count = math.ceil(
                self.extract_total_items_count(response) / self.page_size
            )

        # Em todas as chamadas além da primeira, a resposta é um JSON e portanto o seletores esperados do `response`
        # (.xpath, .css) não estão disponíveis.
        # Então, faço o `response` ser um `Selector` para tê-los de volta onde esperado.
        if has_json_response:
            # Encontra o html que está perdido dentro do JSON.
            # Está dentro do array setValue. O item com field == sc_grid_body tem o html
            html_text = None
            for item in response.json()["setValue"]:
                if item["field"] == "sc_grid_body":
                    html_text = item["value"]

            response = Selector(text=html_text)

        yield from self.consume_table_items(response, pages_consumed)

    def consume_table_items(self, response, pages_consumed):
        """
        Chamado pelo parse_table para identificar todos os links da tabela e gerar uma requisição para cada.
        A requisição na UI abre um modal com links para os documentos.
        """
        # Cada linha tem um link cujo href contem parâmetros para a requisição do conteúdo do modal
        lines = response.xpath('//tr[starts-with(@id, "SC_ancor")]').getall()

        # Impede raspagem da próxima página se algum item com data menor que `self.start_date` apareça na tabela
        should_crawl_next_page = True

        # Raspa cada item da tabela e potencialmente impede que a próxima página seja raspada
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

            # Se data fora dos limites, pula item
            if doc_date < self.start_date or doc_date > self.end_date:
                self.logger.info(f"Pulando item com data ({date_str}) além de limites")

                # Considerando ordenação por data DESC, se data menor que start_date, não existem mais itens
                # dentro dos limites. Pula página
                if doc_date < self.start_date:
                    self.logger.info(
                        f"Detectado item com data ({date_str}) além de start_date. Pulando próxima página"
                    )
                    should_crawl_next_page = False

                continue

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
                f"{self.BASE_URL}/diarioeletronico_form_cliente/?=&=&"
                f"nmgp_outra_jan=true&"
                f"nmgp_url_saida=modal&"
                f"SC_lig_apl_orig=diarioeletronico_grid_cliente&"
                f"nmgp_parms={modal_params}"
            )

            yield scrapy.Request(
                url=modal_url,
                callback=self.parse_modal_items,
                cb_kwargs=item_params,
                priority=10,
            )

        if should_crawl_next_page:
            pages_consumed = pages_consumed + 1
            yield from self.maybe_crawl_next_page(pages_consumed)

    def maybe_crawl_next_page(self, pages_consumed):
        """
        Chamado pelo parse_table para identificar se existem mais páginas a serem consumidas, gerando uma requisição
        para obter a próxima tabela caso exista.
        O Content-Type: application/x-www-form-urlencoded faz o resultado ser um JSON em vez de HTML.
        Parece que o backend tem um bug que faz o resultado HTML sempre retornar os dados da primeira página.
        """
        has_next_page = False

        if pages_consumed <= self.total_pages_count:
            has_next_page = True

        if has_next_page:
            next_page_start = pages_consumed * self.page_size + 1

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
                cb_kwargs={"has_json_response": True, "pages_consumed": pages_consumed},
                priority=1,
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
            return

        self.logger.info(f"Interpretando modal da edição {doc_edition}.")

        # Extrai o href do link dentro do <div id="id_sc_loaded_anexo">
        script_case_init = response.xpath(
            '//form[@name="F1"]//input[@name="script_case_init"]/@value'
        ).get()

        # No caso de edições extras podemos ter 1 ou mais links.
        # Pega a lista de hrefs e texts (innerHtml) deles.
        # Do href é extraído o nome do arquivo a ser usado na requisição.
        # Do text é definido se o diário é uma adição extra.
        link_hrefs = response.xpath('//div[@id="id_sc_loaded_anexo"]//a/@href').getall()
        link_texts = response.xpath(
            '//div[@id="id_sc_loaded_anexo"]//a/text()'
        ).getall()

        for i, href in enumerate(link_hrefs):
            # O segundo parâmetro tem o nome do arquivo que será usado na requisição
            doc_name_match = re.search(r"'documento_db', '(.+?\.pdf)'", href)

            if not doc_name_match:
                continue

            doc_name = doc_name_match.group(1)

            is_extra_edition = False

            # Acessa o text respectivo ao href para definir se é edição extra
            if "COMPLEMENTAR" in link_texts[i]:
                is_extra_edition = True

            url = (
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
                file_urls=[url],
                power="executive",
            )

    def extract_total_items_count(self, response):
        raise NotImplementedError("Implementar na subclasse!")

    def extract_modal_params(self, line):
        raise NotImplementedError("Implementar na subclasse!")
