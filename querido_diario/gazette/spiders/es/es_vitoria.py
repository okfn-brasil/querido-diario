from datetime import date, datetime as dt

from scrapy import FormRequest, Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence, yearly_sequence


class EsVitoriaSpider(BaseGazetteSpider):
    name = "es_vitoria"
    TERRITORY_ID = "3205309"
    allowed_domains = ["diariooficial.vitoria.es.gov.br"]
    start_date = date(2014, 7, 21)

    custom_settings = {
        "DOWNLOAD_DELAY": 0.3,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
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
        for year in yearly_sequence(self.start_date, self.end_date):
            formdata = {
                self.FORM_PARAM_YEAR: str(year),
                "__EVENTTARGET": self.FORM_PARAM_YEAR,
                "__EVENTARGUMENT": "",
            }

            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.make_month_request,
                # We are isolating cookiejar in (year, month) combination
                # to avoid interference between concurrent requests
                meta={"cookiejar": (year)},
            )

    def make_month_request(self, response):
        year = response.meta.get("cookiejar")

        for month_date in monthly_sequence(self.start_date, self.end_date):
            if year == month_date.year:
                formdata = {
                    self.FORM_PARAM_MONTH: str(month_date.month),
                    "__EVENTTARGET": self.FORM_PARAM_MONTH,
                }

                yield FormRequest.from_response(
                    response,
                    formdata=formdata,
                    callback=self.parse_editions_list,
                    meta={"cookiejar": (month_date.year, month_date.month)},
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

                formdata = {
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
