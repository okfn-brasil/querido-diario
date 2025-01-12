import datetime
from urllib.parse import parse_qsl

import scrapy
from dateutil.rrule import MONTHLY, rrule
from parsel import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SeAracajuSpider(BaseGazetteSpider):
    TERRITORY_ID = "2800308"
    name = "se_aracaju"
    start_date = datetime.date(1991, 7, 1)

    custom_settings = {"CONCURRENT_REQUESTS": 12}

    def start_requests(self, cookiejar=None):
        yield scrapy.Request(
            "http://sga.aracaju.se.gov.br:5011/legislacao/faces/diario_form_pesq.jsp",
            meta={"cookiejar": cookiejar} if cookiejar is not None else {},
            dont_filter=True,
            callback=self.make_mandatory_post_request,
        )

    def make_mandatory_post_request(self, response):
        mesano_param = response.css("[value=mesano]::attr(name)").get()

        formdata = {
            # "AJAXREQUEST": "j_id_jsp_1760165330_0",
            # "formPesquisarDiario": "formPesquisarDiario",
            mesano_param: "mesano",
            # "formPesquisarDiario:pesquisa": "",
            # "javax.faces.ViewState": "j_id1",
            # "formPesquisarDiario:j_id_jsp_1760165330_9": "formPesquisarDiario:j_id_jsp_1760165330_9"
        }

        yield scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.start_session_ids,
            dont_filter=True,
            meta={"cookiejar": response.meta.get("cookiejar")},
        )

    def start_session_ids(self, response):
        if not response.meta.get("cookiejar", False):
            rule_start_date = datetime.date(
                self.start_date.year, self.start_date.month, 1
            )
            date_list = list(
                rrule(freq=MONTHLY, dtstart=rule_start_date, until=self.end_date)
            )
            for date in date_list:
                yield from self.start_requests(
                    cookiejar=(
                        date.year,
                        date.month,
                    )
                )
        else:
            yield self.make_year_request(response)

    def make_year_request(self, response):
        self.save_file(response.text, "requisicao_1")

        year, month = cookiejar = response.meta.get("cookiejar")

        container_id = response.css("select::attr(onchange)").re_first(
            r"containerId\':\'(.+)\'"
        )
        mesano_param = response.css("[value=mesano]::attr(name)").get()

        mes_select = response.xpath(
            "//td[contains(./span//text(), 'Mês')]/following-sibling::td//select"
        )
        mes_param = mes_select.xpath("./@name").get()
        mes_value = mes_select.xpath("./option[1]/@value").get()

        ano_param = response.xpath(
            "//td[contains(./span//text(), 'Ano')]/following-sibling::td//select/@name"
        ).get()

        years_param = "formPesquisarDiario:j_id_jsp_1760165330_28"

        return scrapy.FormRequest.from_response(
            response,
            formdata={
                "AJAXREQUEST": container_id,
                # "formPesquisarDiario": "formPesquisarDiario",
                # mesano_param: "mesano",
                mes_param: mes_value,
                # mes_param: str(month),
                ano_param: str(year),
                # javax.faces.ViewState: j_id1
                years_param: years_param,
            },
            dont_filter=True,
            meta={"cookiejar": cookiejar},
            callback=self.make_year_month_request,
        )

    def make_year_month_request(self, response, formdata=None):
        self.save_file(response.text, "requisicao_2")

        year, month = cookiejar = response.meta.get("cookiejar")
        if not formdata:
            container_id = response.css("select::attr(onchange)").re_first(
                r"containerId\':\'(.+)\'"
            )
            mesano_param = response.css("[value=mesano]::attr(name)").get()
            mes_param = response.xpath(
                "//td[contains(./span//text(), 'Mês')]/following-sibling::td//select/@name"
            ).get()
            ano_param = response.xpath(
                "//td[contains(./span//text(), 'Ano')]/following-sibling::td//select/@name"
            ).get()
            search_button_param = response.css(".botaoCadastrarPesq::attr(id)").get()

            formdata = {
                "AJAXREQUEST": container_id,
                # "formPesquisarDiario": "formPesquisarDiario",
                # mesano_param: "mesano",
                mes_param: str(month),
                ano_param: str(year),
                # "javax.faces.ViewState": "j_id2",
                search_button_param: search_button_param,
            }

            # request the first page for the pair (year, month)
            return scrapy.FormRequest.from_response(
                response,
                formdata=formdata,
                dont_filter=True,
                meta={"cookiejar": cookiejar},
                callback=self.parse_page_result,
            )
        else:
            # request the next page from the pagination widget
            return scrapy.FormRequest(
                response.url,
                formdata=formdata,
                meta={"cookiejar": cookiejar},
                callback=self.parse_page_result,
            )

    def parse_page_result(self, response):
        self.save_file(response.text, f"requisicao_3")

        page = Selector(response.text)
        page.remove_namespaces()

        for gazette in page.css(".rich-table-cell"):
            gazette.remove_namespaces()
            gazette_number = gazette.xpath(".//table//td/text()").get()
            if gazette_number is None:
                continue

            raw_date = gazette.css(".rich-panel-header::text").get()
            gazette_date = datetime.datetime.strptime(raw_date, "%d/%m/%Y").date()

            file_url = f"http://sga.aracaju.se.gov.br:5011/diarios/{gazette_number}.pdf"

            if self.start_date <= gazette_date <= self.end_date:
                yield Gazette(
                    date=gazette_date,
                    edition_number=gazette_number,
                    is_extra_edition=False,
                    file_urls=[file_url],
                    power="executive_legislative",
                )

        next_page_param = page.css(".rich-datascr::attr(id)").get()
        next_page = page.css(".rich-datascr-act + .rich-datascr-inact::text").get()
        if next_page_param and next_page:
            last_formdata = dict(parse_qsl(response.request.body.decode()))
            formdata = {
                **last_formdata,
                next_page_param: next_page,
                "AJAX:EVENTS_COUNT": "1",
            }
            yield self.make_year_month_request(response, formdata)

    def save_file(self, dados, nome_arquivo):
        with open(f"{nome_arquivo}.html", "w") as f:
            f.write(dados)
            f.close()
