import datetime
import re
from urllib.parse import urlencode, urlparse, urlunparse

from dateutil.rrule import WEEKLY, rrule
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class EsCariacicaSpider(BaseGazetteSpider):
    zyte_smartproxy_enabled = True

    name = "es_cariacica"
    TERRITORY_ID = "3201308"
    start_date = datetime.date(2014, 7, 1)
    BASE_URL = "https://www.cariacica.es.gov.br/publicacoes/diario-oficial/"

    def start_requests(self):
        search_period = rrule(freq=WEEKLY, dtstart=self.start_date, until=self.end_date)

        for date in search_period:
            start = date.strftime("%Y-%m-%d")
            last_day = date + datetime.timedelta(days=6)

            if last_day.date() > self.end_date:
                end = self.end_date.strftime("%Y-%m-%d")
            else:
                end = last_day.strftime("%Y-%m-%d")

            interval = {"inicio": start, "fim": end}
            url = f"{self.BASE_URL}?{urlencode(interval)}"

            yield Request(url=url, callback=self.parse_week)

    def parse_week(self, response):
        cards_list = response.css("div.card div.card-header")

        for card in cards_list[1:]:
            date = card.xpath("./b/text()").get()
            gazette_date = datetime.datetime.strptime(date, "%d/%m/%Y").date()

            card_content = card.xpath("./following-sibling::table/tr")
            for gazette in card_content[1:]:
                link = response.urljoin(gazette.xpath("./td[4]/a/@href").get())
                gazette_link = self._url_fix(link)

                title = gazette.xpath("./td[1]/text()").get()
                extra_edition = "extra" in title.lower()
                edition = re.search(r"EDIÇÃO (N.+?)?(\d+)", title)
                gazette_edition = edition.group(2) if edition is not None else ""

                yield Gazette(
                    date=gazette_date,
                    file_urls=[gazette_link],
                    is_extra_edition=extra_edition,
                    edition_number=gazette_edition,
                    power="executive_legislative",
                )

    def _url_fix(self, link):
        link = urlparse(link)
        fixed_path = link.path.replace("uploads/2", "uploads//2")
        link = link._replace(scheme="https", path=fixed_path)
        return urlunparse(link)
