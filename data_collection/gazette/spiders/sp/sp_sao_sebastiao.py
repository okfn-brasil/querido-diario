import re
from datetime import date, datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoSebastiaoSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550704"
    name = "sp_sao_sebastiao"
    allowed_domains = ["saosebastiao.sp.gov.br"]
    start_date = date(2017, 3, 15)
    start_urls = ["https://www.saosebastiao.sp.gov.br/doem.asp"]

    def parse(self, response):
        for gazette in response.css("li.document h4.document-title a"):
            gazette_url = f'https://www.saosebastiao.sp.gov.br/{gazette.attrib["href"]}'
            raw_date = re.findall("_(\d{4}\d{2}\d{2})[_\.]", gazette_url)[0]
            parsed_date = datetime.strptime(raw_date, "%Y%m%d").date()

            if not self.start_date <= parsed_date <= self.end_date:
                continue

            gazette_number = re.findall("DOEM_(\d+)_", gazette_url)[0]

            yield Gazette(
                date=parsed_date,
                edition_number=gazette_number,
                is_extra_edition=False,
                power="executive_legislative",
                file_urls=[gazette_url],
            )
