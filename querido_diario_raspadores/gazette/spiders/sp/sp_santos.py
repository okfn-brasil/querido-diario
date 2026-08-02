import datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import daily_sequence


class SpSantosSpider(BaseGazetteSpider):
    TERRITORY_ID = "3548500"
    name = "sp_santos"
    allowed_domains = ["santos.sp.gov.br"]
    start_urls = ["https://diariooficial.santos.sp.gov.br/"]
    download_url = "https://diariooficial.santos.sp.gov.br/edicoes/inicio/download/{}"
    start_date = datetime.date(2001, 5, 5)

    def parse(self, response):
        dates = response.css("#datas.hidden::text").get()

        for date in daily_sequence(self.start_date, self.end_date):
            formatted_date = date.strftime("%Y-%m-%d")
            if formatted_date in dates:
                url = self.download_url.format(formatted_date)
                yield Gazette(
                    date=date.date(),
                    file_urls=[url],
                    is_extra_edition=False,
                    power="executive_legislative",
                )
