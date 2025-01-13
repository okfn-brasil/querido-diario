from datetime import date, datetime

from dateutil.rrule import MONTHLY, rrule, rruleset
from scrapy import FormRequest, Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class EsVitoriaSpider(BaseGazetteSpider):
    name = "es_vitoria"
    TERRITORY_ID = "3205309"    
    allowed_domains = ["diariooficial.vitoria.es.gov.br"]
    start_date = date(2014, 7, 21)

    # When there are too many requests, the server may return
    # an HTTP 406 status code when trying to download a PDF file
    #
    # We set `custom_settings` to avoid triggering the 406 HTTP status code
    # by spreading the downloads for this spider over time

    custom_settings = {
        "DOWNLOAD_DELAY": 0.3,  # 300 ms
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 522, 524, 408, 429, 406],
    }

    FORM_PARAM_YEAR = None
    FORM_PARAM_MONTH = None

    def start_requests(self):
        yield Request(
            "https://diariooficial.vitoria.es.gov.br/",
            callback=self.make_year_request,
        )

    def make_year_request(self, response):
        self.set_form_params(response)     

        monthly_dates = rruleset()
        monthly_dates.rrule(
            rrule(MONTHLY, dtstart=self.start_date, until=self.end_date, bymonthday=[1])
        )
        monthly_dates.rdate(date(self.start_date.year, self.start_date.month, 1))

        for monthly_date in monthly_dates:
            formdata = {self.FORM_PARAM_YEAR: str(monthly_date.year)}

            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.make_month_request,
                # We are isolating cookiejar like (year, month) combination
                # to avoid interference between concurrent requests
                meta={"cookiejar": (monthly_date.year, monthly_date.month)},
            )

    def set_form_params(self, response):
        year_select = response.xpath("//select[contains(@id, 'ddlAno')]")
        self.FORM_PARAM_YEAR = year_select.attrib["name"]

        month_select = response.xpath("//select[contains(@id, 'ddlMes')]")
        self.FORM_PARAM_MONTH = month_select.attrib["name"]


    def make_month_request(self, response):
        year, month = response.meta.get("cookiejar")

        formdata = {
            self.FORM_PARAM_YEAR: str(year),
            self.FORM_PARAM_MONTH: str(month),
            "__EVENTTARGET": self.FORM_PARAM_MONTH,
            "__EVENTARGUMENT": "",
        }

        yield FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.parse_editions_list,
            meta={"cookiejar": response.meta.get("cookiejar")},
        )

    def parse_editions_list(self, response, current_page=1):
        for row in response.xpath("//tbody//td/a[1]"):
            raw_date = row.css("span::text")[0].get().split()[-1]
            gazette_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            if self.start_date <= gazette_date <= self.end_date:
                url = response.urljoin(row.css("a").attrib["href"])

                yield Gazette(
                    date=gazette_date,
                    edition_number="",
                    is_extra_edition=False,
                    file_urls=[url],
                    power="executive",
                )

        has_next_page = (
            response.css(".pagination li")[-1].css("a::text").get() is not None
        )
        if has_next_page:
            next_page = current_page + 1
            year, month = response.meta.get("cookiejar")

            formdata = {
                self.FORM_PARAM_YEAR: str(year),
                self.FORM_PARAM_MONTH: str(month),
                "__EVENTTARGET": self.FORM_PARAM_PAGINATION,
                "__EVENTARGUMENT": f"Page${next_page}",
            }

            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_editions_list,
                cb_kwargs={"current_page": next_page},
                meta={"cookiejar": response.meta.get("cookiejar")},
            )
