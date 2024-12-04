import datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class GoAparecidaDeGoianiaSpider(BaseGazetteSpider):
    TERRITORY_ID = "5201405"
    name = "go_aparecida_de_goiania"
    allowed_domains = ["aparecida.go.gov.br"]
    start_urls = ["https://webio.aparecida.go.gov.br/api/diof/lista"]
    start_date = datetime.date(2014, 8, 1)

    def parse(self, response):
        download_url = "https://webio.aparecida.go.gov.br/diariooficial/download/{}"

        records = response.json()["records"]
        for record in records:
            gazette_url = download_url.format(record["numero"])
            gazette_date = datetime.datetime.strptime(
                record["publicado"], "%Y-%m-%d %H:%M:%S"
            ).date()

            if gazette_date >= self.start_date and gazette_date <= self.end_date:
                yield Gazette(
                    date=gazette_date,
                    file_urls=[gazette_url],
                    is_extra_edition=False,
                    power="executive",
                )
