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
    start_date = datetime.date(1990, 12, 3)

    BASE_URL = "https://gazetamunicipal.cuiaba.mt.gov.br/api/editions"
    # The archive also hosts the state gazette (Diário Oficial do Mato Grosso)
    # and the gazette of the Tribunal de Contas
    EDITION_TYPE = "Gazeta Municipal de Cuiabá"

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    async def start(self):
        for date in monthly_sequence(self.start_date, self.end_date, format="%Y/%m"):
            date_url = f"{self.BASE_URL}/published/{date}"
            yield Request(
                url=date_url,
                headers={
                    "referer": "https://gazetamunicipal.cuiaba.mt.gov.br/",
                },
            )

    def parse(self, response):
        editions = response.json()["editions"]
        for edition in editions:
            if edition.get("edition_type_name") != self.EDITION_TYPE:
                continue

            yield Gazette(
                file_urls=[f"{self.BASE_URL}/downloadPdf/{edition['id']}"],
                date=isoparse(edition["publication_date"]).date(),
                power="executive",
                is_extra_edition=edition["suplement"],
                edition_number=edition["number"],
            )
