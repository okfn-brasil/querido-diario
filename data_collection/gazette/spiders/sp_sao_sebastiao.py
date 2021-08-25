import datetime as dt
import re

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoSebastiaoSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550704"
    name = "sp_sao_sebastiao"
    allowed_domains = ["saosebastiao.sp.gov.br"]
    start_urls = ["http://www.saosebastiao.sp.gov.br/doem.asp"]
    start_date = dt.date(2017, 3, 15)

    # http://www.saosebastiao.sp.gov.br/doem/Diário_Oficial_Eletrônico_038_20170606.pdf
    download_url = "http://www.saosebastiao.sp.gov.br/{}"

    def parse(self, response):
        editions = response.css("h4.document-title a::attr(href)").extract()

        for edition in editions:
            # doem/Diário_Oficial_Eletrônico_038_20170606.pdf

            # edition_date = edition.split("_")[4]
            # 20170606.pdf
            # parsed_date = dateparser.parse(
            #    edition_date[0:8], date_formats=["%Y%m%d"]
            # ).date()

            regex = re.compile(r"_20\d{6}")
            edition_date = regex.search(edition)
            # edition_date = re.search("_20\d{6}", edition)
            # _20170606
            if edition_date:
                parsed_date = dt.datetime.strptime(
                    edition_date.group()[1:], "%Y%m%d"
                ).date()

                self.logger.warning(
                    "EDITION DATE: ||%s|| CONTENT: ||%s||", parsed_date, edition
                )

                url = self.download_url.format(edition)
                yield Gazette(
                    date=parsed_date,
                    file_urls=[url],
                    is_extra_edition=False,
                    power="executive",
                )
            else:
                self.logger.warning("INVALID DATE: ||%s||", edition)
