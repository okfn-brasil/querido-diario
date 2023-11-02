import re
from datetime import date, datetime

from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnNatalSpider(BaseGazetteSpider):
    name = "rn_natal"
    allowed_domains = ["www.natal.rn.gov.br"]
    start_date = date(2003, 11, 19)

    TERRITORY_ID = "2408102"

    def start_requests(self):
        initial_date = date(self.start_date.year, self.start_date.month, 1)
        end_date = self.end_date

        periods_of_interest = [
            (date.year, date.month)
            for date in rrule(freq=MONTHLY, dtstart=initial_date, until=end_date)
        ]

        for year, month in periods_of_interest:
            url = f"http://www.natal.rn.gov.br/api/dom/data/{month:02d}/{year}"
            yield Request(url)

    def parse(self, response):
        for _entry in response.json()["data"]:
            entry = _entry[0]
            url = re.search(r"href='(.+?)'", entry).group(1)
            title = re.search(r">(.+?)<", entry).group(1)
            date = datetime.strptime(title.split(" - ")[-1], "%d/%m/%Y").date()
            extra_edition = (
                re.search("extra|especial", title, re.IGNORECASE) is not None
            )

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=extra_edition,
                power="executive_legislative",
            )
