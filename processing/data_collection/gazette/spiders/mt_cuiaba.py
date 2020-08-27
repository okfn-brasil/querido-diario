import json
from dateparser import parse
from datetime import datetime
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


# based on the website
FIRST_YEAR = 1967
BASE_URL = "https://diariooficial.cuiaba.mt.gov.br/api/api/editions"


class MtCuiabaSpider(BaseGazetteSpider):
    TERRITORY_ID = 5103403
    name = "mt_cuiaba"
    allowed_domains = ["diariooficial.cuiaba.mt.gov.br"]
    start_urls = ["https://diariooficial.cuiaba.mt.gov.br/"]

    def start_requests(self):
        today = datetime.today()
        final_year = today.year
        for year in range(FIRST_YEAR, final_year + 1):
            for month in range(1, 13):
                date_url = f"{BASE_URL}/published/{year}/{month}"
                yield Request(date_url)

    def parse(self, response):
        editions = json.loads(response.text)["editions"]
        for edition in editions:
            edition_id = edition["id"]
            edition_url = f"{BASE_URL}/downloadPdf/{edition_id}"
            edition_date = edition["publication_date"]

            yield Gazette(
                date=parse(edition_date, languages=["pt"]),
                file_urls=[edition_url],
                is_extra_edition=edition["suplement"],
                territory_id=self.TERRITORY_ID,
                power="executive_legislative",
                scraped_at=datetime.utcnow(),
            )
