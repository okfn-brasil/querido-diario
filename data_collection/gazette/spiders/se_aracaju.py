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
        )

    def parse(self, response):
        mesano_param = response.css("[value=mesano]::attr(name)").get()
        yield scrapy.FormRequest.from_response(
            response,
            formdata={mesano_param: "mesano"},
            callback=self.parse_search_by_month_and_year,
            dont_filter=True,
            meta={"cookiejar": response.meta.get("cookiejar")},
        )

    def _make_year_month_request(self, response, formdata=None):
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

        year, month = cookiejar = response.meta.get("cookiejar")
        if not formdata:
            # request the first page for the pair (year, month)
            return scrapy.FormRequest.from_response(
                response,
                formdata={
                    "AJAXREQUEST": container_id,
                    ano_param: str(year),
                    mes_param: str(month),
                    search_button_param: search_button_param,
                },
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

    def parse_search_by_month_and_year(self, response):
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
            yield self._make_year_month_request(response)

    def parse_page_result(self, response):
        page = Selector(response.text)
        page.remove_namespaces()

        for gazette in page.css(".rich-table-cell"):
            gazette.remove_namespaces()
            gazette_number = gazette.xpath(".//table//td/text()").get()
            if gazette_number is None:
                continue

            gazette_date = gazette.css(".rich-panel-header::text").get()
            file_url = f"http://sga.aracaju.se.gov.br:5011/diarios/{gazette_number}.pdf"
            yield Gazette(
                date=datetime.datetime.strptime(gazette_date, "%d/%m/%Y").date(),
                is_extra_edition=False,
                file_urls=[file_url],
                power="executive",
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
            yield self._make_year_month_request(response, formdata)
