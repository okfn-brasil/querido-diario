from datetime import date, datetime

from dateutil.rrule import MONTHLY, rrule, rruleset
from scrapy import FormRequest, Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class EsVitoriaSpider(BaseGazetteSpider):
    name = "es_vitoria"
    TERRITORY_ID = "3205309"
    start_date = date(2014, 7, 21)

    allowed_domains = ["diariooficial.vitoria.es.gov.br"]

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
        self.data_by_monthly_date_by_date = {}

        today = date.today()
        year = today.year
        month = today.month

        yield Request(
            "https://diariooficial.vitoria.es.gov.br/",
            callback=self.make_year_request,
            meta={"cookiejar": f"{self.name}_{year}_{month}"},  # é necessário?
        )

    def make_year_request(self, response):   
        self.set_form_params(response)     

        monthly_dates = rruleset()
        monthly_dates.rrule(
            rrule(MONTHLY, dtstart=self.start_date, until=self.end_date, bymonthday=[1])
        )
        monthly_dates.rdate(date(self.start_date.year, self.start_date.month, 1))

        for monthly_date in monthly_dates:
            
            formdata={
                self.FORM_PARAM_YEAR: str(monthly_date.year)
            }

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
            "__EVENTTARGET": self.FORM_PARAM_MONTH,
            "__EVENTARGUMENT": "",
            self.FORM_PARAM_YEAR: str(year),
            self.FORM_PARAM_MONTH: str(month),
        }

        yield FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.parse_editions_list,
            meta={"cookiejar": response.meta.get("cookiejar")},
        )

    def parse_editions_list(self, response, current_page=1):
        for row in response.xpath("//tbody//td/a[1]"):
            raw_string = row.css("span::text")[0].get()
            date_string_from_text = raw_string.split()[-1]
            gazette_date = self._parse_date(date_string_from_text)

            if not gazette_date:
                self.logger.warning(
                    f"No valid date could be extracted from '{raw_string}'"
                )
                continue

            if gazette_date > self.end_date:
                continue
            elif gazette_date < self.start_date:
                return

            if gazette_date.timetuple()[:2] != current_year_month:
                self.logger.warning(
                    f"Found {gazette_date.isoformat()} gazette while querying"
                    f" for {current_year_month[0]}-{current_year_month[1]:02}"
                    f" period. Skipping..."
                )
                continue

            url = response.urljoin(row.attrib["href"])

            file_urls = self.data_by_monthly_date_by_date.setdefault(
                current_year_month, {}
            ).setdefault(gazette_date, [])

            if url not in file_urls:
                # We use this strategy to avoid duplicates while maintaining row order
                file_urls.append(url)

        number_of_pages = len(
            response.xpath("//ul[contains(@class, 'pagination')]/li").getall()
        )

        if current_page < number_of_pages:
            formdata = {
                "__EVENTARGUMENT": f"Page${next_page}",
                "__EVENTTARGET": "ctl00$conteudo$ucPesquisarDiarioOficial$grdArquivos",
                self.FORM_PARAM_YEAR: str(year),
                self.FORM_PARAM_MONTH: str(month),
            }

            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_editions_list,
                cb_kwargs={
                    "current_year_month": current_year_month,
                    "current_page": current_page + 1,
                },
                # We keep using the same cookiejar for the name_year_month combination
                # because, if we don't, it can interfere with the paging data for
                # a different name_year_month combination
                meta={"cookiejar": f"{self.name}_{year}_{month}"},
            )
        else:
            # After all the entries of the queried year-month period were collected,
            # we finally yield the Gazette per date within that month
            current_year_month_data = self.data_by_monthly_date_by_date.get(
                current_year_month, {}
            )
            for gazette_date, file_urls in current_year_month_data.items():
                yield Gazette(
                    date=gazette_date,
                    is_extra_edition=False,
                    file_urls=file_urls,
                    power="executive",
                )

    def _parse_date(self, raw_date):
        return datetime.strptime(raw_date, "%d/%m/%Y").date()
