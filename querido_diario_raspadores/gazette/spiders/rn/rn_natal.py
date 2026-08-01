import re
from datetime import date, datetime

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class RnNatalSpider(BaseGazetteSpider):
    name = "rn_natal"
    allowed_domains = ["www.natal.rn.gov.br"]
    start_date = date(2003, 11, 19)

    TERRITORY_ID = "2408102"

    def start_requests(self):
        for monthly_date in monthly_sequence(
            self.start_date, self.end_date, format="%m/%Y"
        ):
            yield Request(f"http://www.natal.rn.gov.br/api/dom/data/{monthly_date}")

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
