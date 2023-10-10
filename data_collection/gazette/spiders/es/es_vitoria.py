from datetime import date, datetime

from scrapy import FormRequest, Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

BASE_URL = "https://diariooficial.vitoria.es.gov.br/"


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

    def __init__(self, *args, **kwargs):
        super(EsVitoriaSpider, self).__init__(*args, **kwargs)

        # Period queried for gazette source is based on specific year-month
        # Within a queried period, it has a paging mechanism that can spread multiple files of the same date
        # We collect all the entries for the year-month period to then generate the gazette entries

        # Considering the above descrition, we use a dict named `data_by_monthly_date_by_date`
        # with its keys composed by a 2-tuple
        #     - year
        #     - month
        # and its items is another nested dict composed by
        #     - gazette_date
        # and its items is a list of str representing the URL of the collected files for that date

        # e.g.
        # data_by_monthly_date_by_date = {
        #     (2022, 12): {
        #         date(2022, 12, 2): [
        #             "https://diariooficial.vitoria.es.gov.br/ExibirArquivo.aspx"
        #             "?qs=nnmrXIDe5L4hR81FZwDXlD95Q%2fWHOCtXgeCw%2fnRIrFMxQA7S5mwuf0RM3mOCPGtiwqKwtsQd8WTWmli6Dukj2duE%2bcjGeiOYdOhFAaD2d4lajnB7Bs8eXyta5UTj79FJ",
        #             "https://diariooficial.vitoria.es.gov.br/ExibirArquivo.aspx"
        #             "?qs=nnmrXIDe5L4hR81FZwDXlD95Q%2fWHOCtXgeCw%2fnRIrFMxQA7S5mwuf0RM3mOCPGtiwqKwtsQd8WTWmli6Dukj2duE%2bcjGeiOY4xkUuS2BQabum9G9l8gOaMHLbesi83TO",
        #         ]
        #     }
        # }

        self.data_by_monthly_date_by_date = {}

    def start_requests(self):
        url = BASE_URL

        today = date.today()
        year = today.year
        month = today.month

        yield Request(
            url=url,
            callback=self.initial_parse,
            meta={"cookiejar": f"{self.name}_{year}_{month}"},
        )

    def initial_parse(self, response):
        year_select = response.xpath("//select[contains(@id, 'ddlAno')]")
        year_formkey = year_select.attrib["name"]
        years_available = map(int, year_select.xpath("./option/@value").getall())
        chosen_year = int(
            year_select.xpath("./option[contains(@selected, 'selected')]/@value").get()
        )

        for year in years_available:
            if year < self.start_date.year or self.end_date.year < year:
                continue

            if year == chosen_year:
                yield from self.parse_year(response, year)
                continue

            yield FormRequest.from_response(
                response,
                formdata={year_formkey: str(year)},
                callback=self.parse_year,
                cb_kwargs={"year": year},
                # We are isolating cookiejar per name-year-month combination
                # to avoid interference between concurrent requests
                # Whenever we request a past year, it sets the month to December
                meta={"cookiejar": f"{self.name}_{year}_12"},
            )

    def parse_year(self, response, year):
        year_select = response.xpath("//select[contains(@id, 'ddlAno')]")
        year_formkey = year_select.attrib["name"]

        month_select = response.xpath("//select[contains(@id, 'ddlMes')]")
        month_formkey = month_select.attrib["name"]

        chosen_month = int(
            month_select.xpath("./option[contains(@selected, 'selected')]/@value").get()
        )

        first_day_of_start_date_month = date(
            self.start_date.year, self.start_date.month, 1
        )

        for month in range(1, 13):
            first_day_of_month = date(year, month, 1)
            if (
                first_day_of_month < first_day_of_start_date_month
                or self.end_date < first_day_of_month
            ):
                continue

            current_year_month = (year, month)

            if month == chosen_month:
                yield from self.parse_editions_list(response, current_year_month)
                continue

            formdata = {
                "__EVENTTARGET": month_formkey,
                "__EVENTARGUMENT": "",
                year_formkey: str(year),
                month_formkey: str(month),
            }
            yield FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_editions_list,
                cb_kwargs={
                    "current_year_month": current_year_month,
                },
                # We are isolating cookiejar per name-year-month combination
                # to avoid interference between concurrent requests
                meta={"cookiejar": f"{self.name}_{year}_{month}"},
            )

    def parse_editions_list(
        self,
        response,
        current_year_month,  # (year, month)
        current_page=1,
    ):
        year_select = response.xpath("//select[contains(@id, 'ddlAno')]")
        year_formkey = year_select.attrib["name"]

        month_select = response.xpath("//select[contains(@id, 'ddlMes')]")
        month_formkey = month_select.attrib["name"]

        year, month = current_year_month

        for row in response.xpath(
            "//ancestor::a[span[contains(@id, '_grdArquivos_')]]"
        ):
            raw_string = row.xpath("./span/text()").get()
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
                "__EVENTARGUMENT": f"Page${current_page + 1}",
                "__EVENTTARGET": "ctl00$conteudo$ucPesquisarDiarioOficial$grdArquivos",
                year_formkey: str(year),
                month_formkey: str(month),
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
