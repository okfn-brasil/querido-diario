import datetime as dt

import scrapy
import re

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class CeJuazeiroDoNorteSpider(BaseGazetteSpider):
    TERRITORY_ID = "2307304"
    name = "ce_juazeiro_do_norte"
    allowed_domains = ["juazeiro.ce.gov.br"]
    start_date = None

    def __init__(
        self, start_date: dt.date = None, end_date: dt.date = None, *args, **kwargs
    ):
        self.base_url = "https://juazeiro.ce.gov.br"
        self.start_date = dt.date(year=2009, month=1, day=5)
        self.end_date = dt.date.today()

        super(CeJuazeiroDoNorteSpider, self).__init__(start_date, end_date)

        self.logger.debug(
            "Start date is {date}".format(date=self.start_date.isoformat())
        )
        self.logger.debug("End date is {date}".format(date=self.end_date.isoformat()))

    def start_requests(self):
        """
        This base URL accepts two dates (beginning-date and end-date) or only one date (which will return
        the gazettes for the given date). I will use the second one.
        """
        target_date = self.start_date
        while target_date <= self.end_date:
            formatted_date = target_date.strftime("%d-%m-%Y")
            search_url = f"{self.base_url}/Imprensa/Diario-Oficial/{formatted_date}/"

            yield scrapy.FormRequest(
                url=search_url, method="GET", meta={"date": target_date}
            )
            target_date = target_date + dt.timedelta(days=1)

    def parse(self, response):
        links = [element.attrib["href"] for element in response.css("section.diario a")]
        file_urls = [f"{self.base_url}/{link}" for link in links]
        gazette_date = response.meta["date"]

        if len(links) == 0:
            self.logger.warning(
                "No gazettes found for date {date}".format(date=gazette_date)
            )
        else:
            edition = re.findall(r"/Num(.+?)-", links[0])[0]

            yield Gazette(
                date=gazette_date,
                file_urls=file_urls,
                edition_number=edition,
                power="executive_legislative",
            )
