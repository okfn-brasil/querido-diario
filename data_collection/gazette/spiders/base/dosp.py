import base64
import datetime
import json

import scrapy
from dateutil.rrule import WEEKLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DospGazetteSpider(BaseGazetteSpider):
    allowed_domains = ["dosp.com.br", "imprensaoficialmunicipal.com.br"]

    # Must be defined into child classes
    code = None
    start_date = None

    def start_requests(self):
        for date in rrule(freq=WEEKLY, dtstart=self.start_date, until=self.end_date):
            from_date = date.strftime("%Y-%m-%d")
            to_date = date + datetime.timedelta(days=6)
            to_date = to_date.strftime("%Y-%m-%d")

            yield scrapy.Request(
                f"https://dosp.com.br/api/index.php/dioedata.js/{self.code}/{from_date}/{to_date}?callback=dioe"
            )

    def parse(self, response):
        # The response are in a javascript format, then needs some clean up
        data = json.loads(response.text[6:-2])

        for item in data["data"]:
            code = item["iddo"]
            code = str(code).encode("ascii")
            pdf_code = base64.b64encode(code).decode("ascii")
            file_url = f"https://dosp.com.br/exibe_do.php?i={pdf_code}"
            edition_number = item["edicao_do"]
            date = datetime.datetime.strptime(item["data"], "%Y-%m-%d").date()

            yield Gazette(
                date=date,
                file_urls=[file_url],
                edition_number=edition_number,
                power="executive_legislative",
            )
