import datetime as dt

from parsel import Selector
from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrLondrina(BaseGazetteSpider):
    TERRITORY_ID = "4113700"
    name = "pr_londrina"
    allowed_domains = ["londrina.pr.gov.br"]
    start_urls = ["https://www2.londrina.pr.gov.br/jornaloficial/"]
    start_date = dt.date(1997, 2, 6)

    def _page_request(self, page, start_date, end_date):
        request_data = {
            "option": "com_ajax",
            "module": "web_sampa_search",
            "phrase": "",
            "dateFrom": start_date.strftime("%Y-%m-%d"),
            "dateTo": end_date.strftime("%Y-%m-%d"),
            "category": "",
            "order": "desc",
            "page": f"{page}",
            "format": "raw",
        }
        return FormRequest(
            "https://portal.londrina.pr.gov.br/busca-jornal",
            formdata=request_data,
            cb_kwargs={
                "current_page": page,
                "start_date": start_date,
                "end_date": end_date,
            },
        )

    def start_requests(self):
        start_year = self.start_date.year
        end_year = self.end_date.year

        # We need to send requests grouped by year because if
        # we try to get the whole period, the pagination didn't work
        # correctly and we lost older gazettes (120 pages is the max
        # pagination that works)
        for year in range(start_year, end_year + 1):
            start_date = first_day_of_year = dt.date(year, 1, 1)
            end_date = last_day_of_year = dt.date(year, 12, 31)

            if year == start_year:
                start_date = max([first_day_of_year, self.start_date])
            if year == end_year:
                end_date = min([last_day_of_year, self.end_date])

            yield self._page_request(page=0, start_date=start_date, end_date=end_date)

    def parse(self, response, current_page, start_date, end_date):
        json_data = response.json()

        results = json_data["data"]
        gazettes_selector = Selector(text=results)

        gazette_dates_in_page = set()
        gazettes = gazettes_selector.css("li div.row")
        for gazette in gazettes:
            gazette_url = response.urljoin(gazette.css("a::attr(href)").get())
            raw_date = gazette.css("p::text").re_first(r"(\d{2}\/\d{2}\/\d{4})")
            gazette_date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
            edition_number = gazette.css("a::text").re_first(r"(\d+)")
            is_extra_edition = "extra" in gazette.css("a::text").get().lower()

            gazette_dates_in_page.add(gazette_date)
            if gazette_date > end_date:
                continue

            yield Gazette(
                date=gazette_date,
                file_urls=[
                    gazette_url,
                ],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        if gazette_dates_in_page and min(gazette_dates_in_page) >= start_date:
            # Follow next page in pagination
            next_page = current_page + 1
            yield self._page_request(next_page, start_date, end_date)
