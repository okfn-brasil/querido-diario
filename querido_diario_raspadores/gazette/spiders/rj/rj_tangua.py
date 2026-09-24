import datetime as dt
import re

from scrapy import FormRequest, Request, Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjTanguaSpider(BaseGazetteSpider):
    """Portal da transparência de Tanguá, no sistema Supernova (JSF/PrimeFaces).

    O portal guarda estado no servidor: a listagem de diários só aparece
    depois de acionar o item "Diário oficial" do menu, e o download de cada
    arquivo é um POST que depende da tabela carregada na sessão. Por isso
    cada exercício (ano) é coletado em um cookiejar próprio.
    """

    TERRITORY_ID = "3305752"
    name = "rj_tangua"
    allowed_domains = ["webtangua.supernova.com.br"]
    start_date = dt.date(2022, 1, 4)

    LISTING_URL = (
        "https://webtangua.supernova.com.br:8443"
        "/contaspublicas/pages/publicacao_demais_relatorio.xhtml"
    )
    # Mesma página, pelo mapeamento ".jsf" do JSF: com ".xhtml" na URL, o
    # FilesPipeline salvaria os PDFs com essa extensão.
    DOWNLOAD_URL = LISTING_URL.replace(".xhtml", ".jsf")
    TABLE_ID = "formCenter:demais_relatorios"
    MAX_ROWS_PER_YEAR = 1000
    AJAX_HEADERS = {
        "Faces-Request": "partial/ajax",
        "X-Requested-With": "XMLHttpRequest",
    }

    async def start(self):
        for year in range(self.start_date.year, self.end_date.year + 1):
            # Sem sessão, qualquer página devolve a página inicial do portal.
            yield Request(
                self.LISTING_URL,
                callback=self.parse_home,
                meta={"cookiejar": year},
                cb_kwargs={"year": year},
                dont_filter=True,
            )

    def parse_home(self, response, year):
        source = self._diario_oficial_menu_item(response)
        yield FormRequest.from_response(
            response,
            formid="formCenter",
            formdata=self._ajax_formdata(source, execute="@all"),
            headers=self.AJAX_HEADERS,
            dont_click=True,
            callback=self.parse_menu,
            meta={"cookiejar": year},
            cb_kwargs={"year": year},
            dont_filter=True,
        )

    def parse_menu(self, response, year):
        # O item de menu grava na sessão o tipo de relatório "Diário Oficial";
        # o exercício consultado é escolhido pelo parâmetro da URL.
        yield Request(
            f"{self.LISTING_URL}?exercicio={year}",
            callback=self.parse_listing,
            meta={"cookiejar": year},
            cb_kwargs={"year": year},
            dont_filter=True,
        )

    def parse_listing(self, response, year):
        select_name = response.css(
            "form#formCenter select[name^='formCenter:']::attr(name)"
        ).get()
        report_type = response.xpath(
            f'//select[@name="{select_name}"]/option[contains(text(), "Oficial")]'
            "/@value"
        ).get()
        search_button = response.xpath(
            '//form[@id="formCenter"]//button[.//span[text()="Pesquisar"]]/@id'
        ).get()

        form = {
            "formCenter": "formCenter",
            select_name: report_type,
            "javax.faces.ViewState": response.css(
                "form#formCenter input[name='javax.faces.ViewState']::attr(value)"
            ).get(),
        }
        # A pesquisa já envia os parâmetros de paginação da tabela, pedindo
        # todas as linhas do exercício (cerca de 240 por ano) de uma vez. Isso
        # evita uma requisição extra de paginação e mantém a razão de
        # requisições por item dentro do limite do RequestsItemsRatioMonitor
        # nas coletas diárias.
        pagination = {
            f"{self.TABLE_ID}_pagination": "true",
            f"{self.TABLE_ID}_first": "0",
            f"{self.TABLE_ID}_rows": str(self.MAX_ROWS_PER_YEAR),
            f"{self.TABLE_ID}_encodeFeature": "true",
        }
        yield FormRequest(
            self.LISTING_URL,
            formdata={
                **form,
                **self._ajax_formdata(search_button, execute="@all"),
                **pagination,
            },
            headers=self.AJAX_HEADERS,
            callback=self.parse_table,
            meta={"cookiejar": year},
            cb_kwargs={"year": year, "form": form},
            dont_filter=True,
        )

    def parse_table(self, response, year, form):
        table = Selector(
            text="".join(re.findall(r"<!\[CDATA\[(.*?)\]\]>", response.text, re.S))
        )
        for row in table.css("tr[data-ri]"):
            cells = row.css("td")
            edition_number = cells[1].css("span::text").get("").strip()
            filename = cells[2].css("span::text").get("")

            # Ex.: "Diário Oficial_Nº 1104_Publicação_05012026.pdf", às vezes
            # seguido de "_assinado_<timestamp>" ou "_Edição Extraordinária".
            raw_date = re.search(r"_(\d{8})(?!\d)", filename)
            if raw_date is None:
                self.logger.warning(f"Arquivo sem data no nome: {filename}")
                continue
            gazette_date = dt.datetime.strptime(raw_date.group(1), "%d%m%Y").date()
            if not self.start_date <= gazette_date <= self.end_date:
                continue

            link_id = cells[2].css("a::attr(id)").get()
            # O parâmetro "edicao" é ignorado pelo servidor, mas diferencia a
            # URL de cada arquivo (o FilesPipeline nomeia os arquivos pela URL).
            file_request = FormRequest(
                f"{self.DOWNLOAD_URL}?edicao={edition_number}",
                formdata={**form, link_id: link_id},
                meta={"cookiejar": year},
            )

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition="extraordin" in filename.lower(),
                file_requests=[file_request],
                power="executive",
            )

    def _diario_oficial_menu_item(self, response):
        for link in response.css("a.ui-menuitem-link"):
            label = link.css("span.ui-menuitem-text::text").get("").strip()
            if re.fullmatch(r"- Di.rio oficial", label, re.IGNORECASE):
                return re.search(r's:"([^"]+)"', link.attrib["onclick"]).group(1)
        raise ValueError("Item de menu 'Diário oficial' não encontrado")

    def _ajax_formdata(self, source, execute):
        return {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": source,
            "javax.faces.partial.execute": execute,
            "javax.faces.partial.render": "formCenter",
            source: source,
        }
