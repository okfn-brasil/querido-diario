import re
from base64 import b64encode
from datetime import datetime
from json import loads

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseDospSpider(BaseGazetteSpider):
    allowed_domains = ["dosp.com.br", "imprensaoficialmunicipal.com.br"]

    def __init__(self, *args, **kwargs):
        super(BaseDospSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.GAZETTES_PAGE_URL]

    def parse(self, response):
        code = re.search(r"urlapi\+'.js/(\d*)/'\+idsecao\+'", response.text).group(1)
        yield scrapy.Request(
            f"https://dosp.com.br/api/index.php/dioe.js/{code}",
            callback=self.parse_json,
        )

    def parse_json(self, response):
        json_text = (
            response.css("p::text").get().replace("parseResponse(", "")
        ).replace(");", "")

        json_text = loads(json_text)

        for diarios in json_text["data"]:
            data = datetime.strptime(diarios["data"], "%Y-%m-%d").date()
            code_link = str(diarios["iddo"]).encode("ascii")
            code_link = b64encode(code_link).decode("ascii")

            if self.start_date <= data <= self.end_date:
                file_url = f"https://dosp.com.br/exibe_do.php?i={code_link}.pdf"
                yield Gazette(
                    date=data,
                    power="executivo",
                    edition_number=diarios["edicao_do"],
                    is_extra_edition=diarios["flag_extra"] > 0,
                    granularity="individual",
                    act_category="",
                    publishing_body="",
                    document_code="",
                    document_page="",
                    file_urls=[file_url],
                )
