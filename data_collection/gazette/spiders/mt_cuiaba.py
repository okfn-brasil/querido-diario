import datetime

from dateutil.parser import isoparse
from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


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
        for date in rrule(MONTHLY, dtstart=self.start_date, until=self.end_date):
            date_url = f"{self.BASE_URL}/published/{date.year}/{date.month}"
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
