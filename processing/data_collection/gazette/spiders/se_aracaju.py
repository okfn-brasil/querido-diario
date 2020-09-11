from datetime import datetime
from parsel import Selector

from gazette.spiders.base import BaseGazetteSpider

from gazette.items import Gazette
from dateparser import parse
import scrapy


class SeAracajuSpider(BaseGazetteSpider):
    TERRITORY_ID = "2800308"
    name = "se_aracaju"

    custom_settings = {"CONCURRENT_REQUESTS": 1}

    start_urls = [
        "http://sga.aracaju.se.gov.br:5011/legislacao/faces/diario_form_pesq.jsp"
    ]

    def parse(self, response):
        mesano_param = response.css("[value=mesano]::attr(name)").get()
        yield scrapy.FormRequest.from_response(
            response,
            formdata={mesano_param: "mesano"},
            callback=self.parse_search_by_month_and_year,
        )

    def parse_search_by_month_and_year(self, response):
        all_years_available = response.xpath(
            "//td[contains(./span//text(), 'Ano')]/following-sibling::td//option/@value"
        ).getall()

        container_id = response.css("select::attr(onchange)").re_first(
            r"containerId\':\'(.+)\'"
        )
        mes_param = response.xpath(
            "//td[contains(./span//text(), 'Mês')]/following-sibling::td//select/@name"
        ).get()
        ano_param = response.xpath(
            "//td[contains(./span//text(), 'Ano')]/following-sibling::td//select/@name"
        ).get()
        search_button_param = response.css(".botaoCadastrarPesq::attr(id)").get()

        for year in all_years_available:
            for month in range(1, 13):
                yield scrapy.FormRequest.from_response(
                    response,
                    formdata={
                        "AJAXREQUEST": container_id,
                        ano_param: str(year),
                        mes_param: str(month),
                        search_button_param: search_button_param,
                    },
                    callback=self.parse_page_result,
                )

    def parse_page_result(self, response):
        gazettes = response.css(".rich-table-cell")
        for gazette in gazettes:
            gazette.remove_namespaces()
            gazette_number = gazette.xpath(".//table//td/text()").get()
            if gazette_number is None:
                continue

            gazette_date = gazette.css(".rich-panel-header::text").get()
            file_url = f"http://sga.aracaju.se.gov.br:5011/diarios/{gazette_number}.pdf"
            yield Gazette(
                date=parse(gazette_date, languages=["pt"]).date(),
                is_extra_edition=False,
                territory_id=self.TERRITORY_ID,
                file_urls=[file_url],
                power="executive",
                scraped_at=datetime.utcnow(),
            )

    # def parse_page(self, response, ano_param, mes_param, container_id, botao):
    #     gazettes = response.css(".rich-table-cell")
    #     for gazette in gazettes:
    #         gazette.remove_namespaces()

    #         gazette_number = gazette.xpath(".//table//td/text()").get()
    #         gazette_date = gazette.css(".rich-panel-header::text").get()

    #         file_url = f"http://sga.aracaju.se.gov.br:5011/diarios/{gazette_number}.pdf"
    # yield Gazette(
    #     date=parse(gazette_date, languages=["pt"]).date(),
    #     is_extra_edition=False,
    #     territory_id=self.TERRITORY_ID,
    #     file_urls=[file_url],
    #     power="executive",
    #     scraped_at=datetime.utcnow(),
    # )

    # sel = Selector(text=response.text, type="xml")
    # sel.remove_namespaces()
    # pages = sel.css("tfoot td::attr(onclick)").re(r"page\': \'([0-9]+)\'")
    # page_param = sel.css(".rich-datascr::attr(id)").get()

    # import requests

    # cookies = {
    #     'JSESSIONID': 'AF8EC5AA0D0458558C47EC552A764D06',
    #     '__utma': '110275463.170343355.1598525926.1598525926.1598926208.2',
    #     '__utmz': '110275463.1598525926.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    #     '__utmb': '110275463.1.10.1598926208',
    #     '__utmc': '110275463',
    #     '__utmt': '1',
    # }

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    #     'Accept': '*/*',
    #     'Accept-Language': 'en-US,en;q=0.5',
    #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #     'Origin': 'http://sga.aracaju.se.gov.br:5011',
    #     'Connection': 'keep-alive',
    #     'Referer': 'http://sga.aracaju.se.gov.br:5011/legislacao/faces/diario_form_pesq.jsp',
    # }

    # response = requests.post('http://sga.aracaju.se.gov.br:5011/legislacao/faces/diario_form_pesq.jsp;jsessionid=AF8EC5AA0D0458558C47EC552A764D06', headers=headers, cookies=cookies, data=data)

    # for page in pages:
    #     import ipdb

    #     ipdb.set_trace()
    #     yield scrapy.FormRequest(
    #         response.url,
    #         formdata={
    #             "AJAXREQUEST": container_id,
    #             ano_param: str("2020"),
    #             mes_param: str("8"),
    #             botao: botao,
    #             page_param: page,
    #         },
    #         callback=self.parse_next_page,
    #     )

    # formPesquisarDiario:j_id_jsp_1760165330_6

    # data = {
    #   'AJAXREQUEST': 'j_id_jsp_1760165330_0',
    #   'formPesquisarDiario': 'formPesquisarDiario',
    #   'formPesquisarDiario:j_id_jsp_1760165330_6': 'mesano',
    #   'formPesquisarDiario:j_id_jsp_1760165330_22': '8',
    #   'formPesquisarDiario:j_id_jsp_1760165330_25': '2020',
    #   'javax.faces.ViewState': 'j_id1',
    #   'formPesquisarDiario:j_id_jsp_1760165330_31:j_id_jsp_1760165330_41': '2',
    #   'ajaxSingle': 'formPesquisarDiario:j_id_jsp_1760165330_31:j_id_jsp_1760165330_41',
    #   'AJAX:EVENTS_COUNT': '1',
    #   '': ''
    # }

    # def parse_next_page(self, response):
    #     import ipdb

    #     ipdb.set_trace()


# TODO
# - Processar paginação
# - Verificar o link de diários antigos - que parecem que não seguem o padrão {numero}.pdf
# - Gerenciamentyo de sessões.
