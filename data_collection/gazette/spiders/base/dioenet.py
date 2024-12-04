import re
from collections import deque
from datetime import datetime
from itertools import islice

from dateutil.rrule import WEEKLY, rrule
from scrapy.http import FormRequest, Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseDioenetSpider(BaseGazetteSpider):
    """
    Base spider for all cities listed on https://plenussistemas.dioenet.com.br
    """

    allowed_domains = ["plenussistemas.dioenet.com.br"]

    def start_requests(self):
        dates_of_interest = [
            dt
            for dt in rrule(freq=WEEKLY, dtstart=self.start_date, until=self.end_date)
        ]

        if self.end_date not in dates_of_interest:
            dates_of_interest.append(self.end_date)

        for start, end in self._sliding_window(dates_of_interest, 2):
            params = {
                "d": f"{start.strftime('%d/%m/%Y')} a {end.strftime('%d/%m/%Y')}",
                "pagina": "1",
            }

            yield FormRequest(
                url=self.BASE_URL,
                method="GET",
                formdata=params,
                cb_kwargs={"params": params},
            )

    def parse(self, response, params):
        for gazette in response.css("ul.lista-diarios li"):
            # can return ['Edição nº 841'] or ['Edição nº 842', 'Extra']
            raw_edition = gazette.css(".col-one span::text").getall()
            gazette_number = re.findall("\d+", raw_edition[0])[0]
            gazette_extra = True if "Extra" in raw_edition else False

            elem = gazette.css(".col-two a.btn")
            gazette_url = elem.attrib["href"]
            raw_date = re.findall("(\d{2}/\d{2}/\d{4})", elem.attrib["title"])[0]
            gazette_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            gazette_item = {
                "date": gazette_date,
                "edition_number": gazette_number,
                "is_extra_edition": gazette_extra,
                "power": self.power,
            }

            yield Request(
                gazette_url,
                callback=self.get_gazette_url,
                cb_kwargs={"gazette_item": gazette_item},
            )

        if response.css("ul.pagination li.next.page"):
            params["pagina"] = f"{int(params['pagina'])+1}"

            yield FormRequest(
                url=self.BASE_URL,
                method="GET",
                formdata=params,
                cb_kwargs={"params": params},
            )

    def get_gazette_url(self, response, gazette_item):
        gazette_url = response.xpath("//iframe/@src").get()
        gazette_url = re.search(r"file=(.*)", gazette_url).group(1)

        yield Gazette(
            **gazette_item,
            file_urls=[gazette_url],
        )

    def _sliding_window(self, iterable, n):
        it = iter(iterable)
        window = deque(islice(it, n - 1), maxlen=n)
        for x in it:
            window.append(x)
            yield tuple(window)
