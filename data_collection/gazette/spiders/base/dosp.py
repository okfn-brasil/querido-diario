from base64 import b64encode
from datetime import datetime
from json import loads

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DospGazetteSpider(BaseGazetteSpider):
    # Must be defined into child classes
    code = None
    start_date = None

    allowed_domains = ["dosp.com.br"]
    end_date = datetime.today().date()

    def start_requests(self):
        yield scrapy.Request(f"https://dosp.com.br/api/index.php/dioe.js/{self.code}")

    def parse(self, response):
        json_text = (
            response.css("p::text").get().replace("parseResponse(", "")
        ).replace(");", "")

        json_text = loads(json_text)

        for diarios in json_text["data"]:
            data = datetime.strptime(diarios["data"], "%Y-%m-%d").date()
            code_link = str(diarios["iddo"]).encode("ascii")
            code_link = b64encode(code_link).decode("ascii")

            if self.start_date <= data <= self.end_date:
                yield Gazette(
                    date=data,
                    edition_number=diarios["edicao_do"],
                    file_urls=[
                        f"https://dosp.com.br/exibe_do.php?i={code_link}.pdf",
                    ],
                    is_extra_edition=diarios["flag_extra"] > 0,
                    power="executive",
                )
