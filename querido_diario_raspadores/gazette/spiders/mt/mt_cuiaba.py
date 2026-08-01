import datetime

from dateutil.parser import isoparse
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class MtCuiabaSpider(BaseGazetteSpider):
    TERRITORY_ID = "5103403"
    name = "mt_cuiaba"
    allowed_domains = ["gazetamunicipal.cuiaba.mt.gov.br"]
    start_date = datetime.date(1967, 1, 1)

    BASE_URL = "http://gazetamunicipal.cuiaba.mt.gov.br/api/api/editions"

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def start_requests(self):
        for date in monthly_sequence(self.start_date, self.end_date, format="%Y/%m"):
            date_url = f"{self.BASE_URL}/published/{date}"
            yield Request(
                url=date_url,
                headers={
                    "referer": "https://diariooficial.cuiaba.mt.gov.br/edicoes",
                },
            )

    def parse(self, response):
        editions = response.json()["editions"]
        for edition in editions:
            yield Gazette(
                file_urls=[f"{self.BASE_URL}/downloadPdf/{edition['id']}"],
                date=isoparse(edition["publication_date"]).date(),
                power="executive",
                is_extra_edition=edition["suplement"],
                edition_number=edition["number"],
            )
