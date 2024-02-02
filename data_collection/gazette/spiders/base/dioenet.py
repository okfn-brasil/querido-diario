import re
from datetime import datetime

from dateutil.rrule import DAILY, rrule
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DionetGazetteSpider(BaseGazetteSpider):
    """
    Base spider for all cities listed on https://plenussistemas.dioenet.com.br
    """

    allowed_domains = ["plenussistemas.dioenet.com.br"]

    def start_requests(self):
        # sp_tabute -> taubate
        # ap_pedra_branca_do_amapari -> pedra-branca-do-amapari
        city = "-".join(self.name.split("_")[1:])
        for daily_date in rrule(
            freq=DAILY, dtstart=self.start_date, until=self.end_date
        ):
            yield Request(
                f'https://plenussistemas.dioenet.com.br/list/{city}?&d={daily_date.strftime("%d/%m/%Y")}'
            )

    def parse(self, response):
        for gazette in response.css("ul.lista-diarios li"):
            # can return ['Edição nº 841'] or ['Edição nº 842', 'Extra']
            desc = gazette.css(".col-one span::text").getall()
            gazette_number = re.findall("\d+", desc[0])[0]
            gazette_extra = True if "Extra" in desc else False

            elem = gazette.css(".col-two a.btn")
            gazette_url = elem.attrib["href"]
            raw_date = re.findall("(\d{2}/\d{2}/\d{4})", elem.attrib["title"])[0]
            gazette_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_number,
                is_extra_edition=gazette_extra,
                power="executive_legislative",
                file_urls=[gazette_url],
            )
