import re
from datetime import date

import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoSebastiaoSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550704"
    name = "sp_sao_sebastiao"
    allowed_domains = ["saosebastiao.sp.gov.br"]
    start_urls = ["http://www.saosebastiao.sp.gov.br/doem.asp"]
    start_date = date(2017, 3, 15)
    end_date = None

    download_url = "http://www.saosebastiao.sp.gov.br/{}"

    def parse(self, response):
        editions = response.css("h4.document-title a::attr(href)").getall()

        regex = re.compile(r"_20\d{6}")
        for edition in editions:

            edition_date = regex.search(edition)
            if edition_date:
                print(f"ERRO: |{edition_date.group()[1:]}|")
                parsed_date = dateparser.parse(
                    edition_date.group()[1:], languages=["pt"], date_formats=["%Y%m%d"]
                ).date()

                url = self.download_url.format(edition)
                yield Gazette(
                    date=parsed_date,
                    file_urls=[url],
                    is_extra_edition=False,
                    power="executive",
                )
            else:
                print(f"Invalid date: {edition}")
