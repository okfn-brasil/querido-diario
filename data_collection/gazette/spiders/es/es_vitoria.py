from datetime import date, datetime as dt

from dateutil.rrule import MONTHLY, YEARLY, rrule, rruleset
from scrapy import FormRequest, Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class EsVitoriaSpider(BaseGazetteSpider):
    name = "es_vitoria"
    TERRITORY_ID = "3205309"
    allowed_domains = ["diariooficial.vitoria.es.gov.br"]
    start_date = date(2014, 7, 21)

    custom_settings = {
        "DOWNLOAD_DELAY": 0.3,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 522, 524, 408, 429, 406],
    }

    FORM_PARAM_YEAR = "ctl00$conteudo$ucPesquisarDiarioOficial$ddlAno"
    FORM_PARAM_MONTH = "ctl00$conteudo$ucPesquisarDiarioOficial$ddlMes"
    FORM_PARAM_PAGINATION = "ctl00$conteudo$ucPesquisarDiarioOficial$grdArquivos"

    def start_requests(self):
        yield Request(
            "https://diariooficial.vitoria.es.gov.br/",
            callback=self.make_year_request,
        )

    def make_year_request(self, response):
        for yearly_date in self._dates_of_interest(YEARLY):
            formdata = {
                self.FORM_PARAM_YEAR: str(yearly_date.year),
                "__EVENTTARGET": self.FORM_PARAM_YEAR,
                "__EVENTARGUMENT": "",
            }

            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.make_month_request,
                # We are isolating cookiejar in (year, month) combination
                # to avoid interference between concurrent requests
                meta={"cookiejar": (yearly_date.year)},
            )

    def make_month_request(self, response):
        year = response.meta.get("cookiejar")

        for monthly_date in self._dates_of_interest(MONTHLY):
            if dt(year, 1, 1) <= monthly_date <= dt(year, 12, 31):

                formdata = {
                    self.FORM_PARAM_YEAR: str(monthly_date.year),
                    self.FORM_PARAM_MONTH: str(monthly_date.month),
                    "__EVENTTARGET": self.FORM_PARAM_MONTH,
                    "__EVENTARGUMENT": "",
                }

                yield FormRequest.from_response(
                    response,
                    formdata=formdata,
                    callback=self.parse_editions_list,
                    meta={"cookiejar": (monthly_date.year, monthly_date.month)},
                )

    def parse_editions_list(self, response, current_page=1):
        for row in response.xpath("//tbody//td/a[1]"):
            raw_date = row.css("span::text")[0].get().split()[-1]
            gazette_date = dt.strptime(raw_date, "%d/%m/%Y").date()

            if self.start_date <= gazette_date <= self.end_date:
                url = response.urljoin(row.css("a").attrib["href"])

                yield Gazette(
                    date=gazette_date,
                    edition_number="",
                    is_extra_edition=False,
                    file_urls=[url],
                    power="executive",
                )

        if "pagination" in response.text:
            if response.css(".pagination li")[-1].css("a::text").get():
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

    def _dates_of_interest(self, recurrence):
        dates = rruleset()
        dates.rrule(rrule(recurrence, dtstart=self.start_date, until=self.end_date, bymonthday=[1]))
        dates.rdate(dt(self.start_date.year, self.start_date.month, 1))
        return dates