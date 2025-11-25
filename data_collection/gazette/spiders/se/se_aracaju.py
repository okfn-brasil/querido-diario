import ast
import datetime
from urllib.parse import parse_qsl

import scrapy
from parsel import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class SeAracajuSpider(BaseGazetteSpider):
    TERRITORY_ID = "2800308"
    name = "se_aracaju"
    start_date = datetime.date(1991, 7, 1)
    allowed_domains = ["aracaju.se.gov.br"]

    custom_settings = {"CONCURRENT_REQUESTS_PER_DOMAIN": 12}

    def start_requests(self, cookiejar=None):
        yield scrapy.Request(
            "http://sga.aracaju.se.gov.br:5011/legislacao/faces/diario_form_pesq.jsp",
            meta={"cookiejar": cookiejar} if cookiejar is not None else {},
            dont_filter=True,
            callback=self.make_mandatory_post_request,
        )

    def make_mandatory_post_request(self, response):
        search_option_field = response.css("[value=mesano]::attr(name)").get()
        yield scrapy.FormRequest.from_response(
            response,
            formdata={search_option_field: "mesano"},
            callback=self.start_session_ids,
            dont_filter=True,
            meta={"cookiejar": response.meta.get("cookiejar")},
        )

    def start_session_ids(self, response):
        if not response.meta.get("cookiejar", False):
            for date in monthly_sequence(self.start_date, self.end_date):
                yield from self.start_requests(
                    cookiejar=(
                        date.year,
                        date.month,
                    )
                )
        else:
            yield self.make_year_request(response)

    def make_year_request(self, response):
        month_select = response.css("select")[0]
        month_field = month_select.attrib["name"]
        month_value = month_select.css("option").attrib["value"]

        year_select = response.css("select")[1]
        year_field = year_select.attrib["name"]
        year_params_string = year_select.css("::attr(onchange)").re_first(r"{.+}")
        year_params = ast.literal_eval(year_params_string)
        year_search_field = year_params["similarityGroupingId"]

        ajaxrequest_value = year_params["containerId"]
        general_field = year_field.split(":")[0]
        search_option_field = response.css("[value=mesano]::attr(name)").get()

        formdata = {
            "AJAXREQUEST": ajaxrequest_value,
            general_field: general_field,
            search_option_field: "mesano",
            month_field: month_value,
            year_field: str(response.meta.get("cookiejar")[0]),
            year_search_field: year_search_field,
        }

        return scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            dont_filter=True,
            meta={"cookiejar": response.meta.get("cookiejar")},
            callback=self.make_year_month_request,
            cb_kwargs={
                "month_field": month_field,
                "year_search_field": year_search_field,
            },
        )

    def make_year_month_request(
        self, response, formdata=None, month_field=None, year_search_field=None
    ):
        if not formdata:  # request the first page for the pair (year, month)
            search_button_field = response.css(".botaoCadastrarPesq::attr(id)").get()

            formdata = dict(parse_qsl(response.request.body.decode()))
            del formdata[year_search_field]
            formdata[search_button_field] = search_button_field
            formdata[month_field] = str(response.meta.get("cookiejar")[1])

        return scrapy.FormRequest(
            response.url,
            formdata=formdata,
            dont_filter=True,
            meta={"cookiejar": response.meta.get("cookiejar")},
            callback=self.parse_page_result,
        )

    def parse_page_result(self, response):
        page = Selector(response.text)
        page.remove_namespaces()

        for gazette in page.css(".rich-table-cell"):
            raw_date = gazette.css(".rich-panel-header::text").get()
            if raw_date is not None:
                gazette_date = datetime.datetime.strptime(raw_date, "%d/%m/%Y").date()
                gazette_number = gazette.xpath(".//table//td/text()").get()

                if self.start_date <= gazette_date <= self.end_date:
                    # some daily boxes has more than one edition
                    for raw_info in gazette.css("table tbody .label::text")[1:]:
                        if "Suplementar" in raw_info.get():
                            is_extra_edition = True
                            file_url = f"http://sga.aracaju.se.gov.br:5011/diarios/{gazette_number}S.pdf"
                        else:
                            is_extra_edition = False
                            file_url = f"http://sga.aracaju.se.gov.br:5011/diarios/{gazette_number}.pdf"

                        yield Gazette(
                            date=gazette_date,
                            edition_number=gazette_number,
                            is_extra_edition=is_extra_edition,
                            file_urls=[file_url],
                            power="executive_legislative",
                        )

        next_page_field = page.css(".rich-datascr::attr(id)").get()
        next_page = page.css(".rich-datascr-act + .rich-datascr-inact::text").get()
        if next_page_field and next_page:
            last_formdata = dict(parse_qsl(response.request.body.decode()))
            formdata = {
                **last_formdata,
                next_page_field: next_page,
                "ajaxSingle": next_page_field,
                "AJAX:EVENTS_COUNT": "1",
            }
            yield self.make_year_month_request(response, formdata)
