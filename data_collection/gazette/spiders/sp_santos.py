import datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSantosSpider(BaseGazetteSpider):
    TERRITORY_ID = "3548500"
    name = "sp_santos"
    allowed_domains = ["santos.sp.gov.br"]
    start_urls = ["https://diariooficial.santos.sp.gov.br/"]
    download_url = "https://diariooficial.santos.sp.gov.br/edicoes/inicio/download/{}"
    start_date = datetime.date(2001, 5, 5)

    def parse(self, response):
        dates = response.css("#datas.hidden::text").get()

        while self.end_date >= self.start_date:
            if str(parsing_date) in dates:
                url = self.download_url.format(parsing_date)
                yield Gazette(
                    date=parsing_date,
                    file_urls=[url],
                    is_extra_edition=False,
                    power="executive_legislative",
                )

            parsing_date = parsing_date - datetime.timedelta(days=1)
