import scrapy
import json
from dateparser import parse
from datetime import datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


# based on the website
FIRST_YEAR = 1967


class MtCuiabaSpider(BaseGazetteSpider):
    TERRITORY_ID = 5103403
    name = "mt_cuiaba"
    allowed_domains = ["diariooficial.cuiaba.mt.gov.br"]
    start_urls = ["https://diariooficial.cuiaba.mt.gov.br/edicoes"]

    def start_requests(self):
        date_url = "https://diariooficial.cuiaba.mt.gov.br/api/api/editions/published/{year}/{month}"
        today = datetime.today()
        final_year = today.year
        for year in range(FIRST_YEAR, final_year + 1):
            for month in range(1, 13):
                url = date_url.format(year=year, month=month)
                yield scrapy.Request(url)

    def parse(self, response):
        base_url = (
            "https://diariooficial.cuiaba.mt.gov.br/api/api/editions/downloadPdf/{}"
        )
        editions = json.loads(response.text)["editions"]
        for edition in editions:
            edition_id = edition["id"]
            edition_url = base_url.format(edition_id)
            edition_date = edition["publication_date"]

            yield Gazette(
                date=parse(edition_date, languages=["pt"]),
                file_urls=[edition_url],
                is_extra_edition=edition["suplement"],
                territory_id=self.TERRITORY_ID,
                power="executive_legislative",
                scraped_at=datetime.utcnow(),
            )
