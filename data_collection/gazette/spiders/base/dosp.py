import base64
import datetime
import json

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DospGazetteSpider(BaseGazetteSpider):
    allowed_domains = ["dosp.com.br", "imprensaoficialmunicipal.com.br"]

    # Must be defined into child classes
    code = None
    start_date = None

    def start_requests(self):
        FORMAT_DATE = "%Y-%m-%d"
        target_date = self.start_date
        end_date = datetime.date.today()

        while target_date <= end_date:
            from_data = target_date.strftime(FORMAT_DATE)
            target_date = target_date + datetime.timedelta(weeks=1)
            to_date = target_date.strftime(FORMAT_DATE)

            yield scrapy.Request(
                f"https://dosp.com.br/api/index.php/dioedata.js/{self.code}/{from_data}/{to_date}?callback=dioe"
            )

    def parse(self, response):
        # The response are in a javascript format, then needs some clean up
        data = json.loads(response.text[6:-2])

        for item in data["data"]:
            code = item["iddo"]
            code = str(code).encode("ascii")
            pdf_code = base64.b64encode(code).decode("ascii")
            file_url = "https://dosp.com.br/exibe_do.php?i=" + pdf_code
            edition_number = item["edicao_do"]
            date = dateparser.parse(item["data"]).date()

            yield Gazette(
                date=date,
                file_urls=[file_url],
                edition_number=edition_number,
                power="executive_legislative",
            )
