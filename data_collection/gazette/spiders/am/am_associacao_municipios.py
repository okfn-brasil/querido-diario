import datetime as dt

import scrapy
from dateutil import rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AmAssociacaoMunicipiosSpider(BaseGazetteSpider):
    TERRITORY_ID = "1300000"
    name = "am_associacao_municipios"
    allowed_domains = ["https://diariomunicipalaam.org.br/"]
    download_url = "https://diariomunicipalaam.org.br/visualizar-publicacao/{}"
    start_date = dt.date(2009, 10, 19)  # primeira edição encontrada
    end_date = dt.date.today()

    def start_requests(self):
        for date in rrule.rrule(
            rrule.DAILY, dtstart=self.start_date, until=self.end_date
        ):
            formatted_date = date.strftime("%Y%m%d")  # Formato YYYYMMDD
            url = self.download_url.format(formatted_date)
            yield scrapy.Request(
                url,
                method="HEAD",
                callback=self.parse_valid_gazette_file,
                cb_kwargs={"gazette_date": date.date()},
            )

    def parse_valid_gazette_file(self, response, gazette_date):
        if response.status == 200:
            yield Gazette(
                date=gazette_date,
                file_urls=[response.url],
                is_extra_edition=False,
                power="executive",
            )
