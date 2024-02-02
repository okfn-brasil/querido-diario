from datetime import date, datetime

from dateutil.rrule import DAILY, rrule
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoJoseDosCamposSpider(BaseGazetteSpider):
    name = "sp_sao_jose_dos_campos"
    TERRITORY_ID = "3549904"
    allowed_domains = ["diariodomunicipio.sjc.sp.gov.br"]
    api_url = "https://diariodomunicipio.sjc.sp.gov.br/apifront/portal/edicoes/edicoes_from_data/"
    start_date = date(2015, 8, 7)

    def start_requests(self):
        for daily_date in rrule(
            freq=DAILY, dtstart=self.start_date, until=self.end_date
        ):
            url = f'{self.api_url}{daily_date.strftime("%Y-%m-%d")}.json'

            yield Request(url)

    def parse(self, response):
        data = response.json()
        if data["erro"]:
            return
        for gazzete in data["itens"]:
            yield Gazette(
                date=datetime.strptime(gazzete["data"], "%d/%m/%Y").date(),
                edition_number=gazzete["numero"],
                is_extra_edition=gazzete["suplemento"] != 0
                and gazzete["suplemento"] != "",
                power="executive_legislative",
                file_urls=[
                    f'https://diariodomunicipio.sjc.sp.gov.br/portal/edicoes/download/{gazzete["id"]}'
                ],
            )
