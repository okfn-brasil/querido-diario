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
    # and the gazette of the Tribunal de Contas (TCE-MT). Between the last
    # edition of the old Gazeta Municipal series (2013-05-03, nº 1209) and the
    # first of the new one (2020-10-26, nº 1), the city published its acts in
    # the TCE-MT gazette, so only in this period it is collected
    MUNICIPAL_GAZETTE = "Gazeta Municipal de Cuiabá"
    TCE_GAZETTE = "Diário Oficial do Tribunal de Contas"
    TCE_GAZETTE_PERIOD = (datetime.date(2013, 5, 4), datetime.date(2020, 10, 25))

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
            gazette_date = isoparse(edition["publication_date"]).date()
            if not self._is_municipal_gazette(edition, gazette_date):
                continue

            yield Gazette(
                file_urls=[f"{self.BASE_URL}/downloadPdf/{edition['id']}"],
                date=gazette_date,
                power="executive",
                is_extra_edition=edition["suplement"],
                edition_number=edition["number"],
            )

    def _is_municipal_gazette(self, edition, gazette_date):
        edition_type = edition.get("edition_type_name")
        if edition_type == self.MUNICIPAL_GAZETTE:
            return True
        start, end = self.TCE_GAZETTE_PERIOD
        return edition_type == self.TCE_GAZETTE and start <= gazette_date <= end
