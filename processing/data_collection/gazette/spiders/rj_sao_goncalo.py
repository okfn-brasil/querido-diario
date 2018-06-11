import datetime

from gazette.spiders.base import BaseGazetteSpider
from gazette.items import Gazette


class RjSaoGoncaloSpider(BaseGazetteSpider):
    TERRITORY_ID = '3304904'
    name = 'rj_sao_goncalo'
    allowed_domains = ['www.pmsg.rj.gov.br']
    download_gazette_url = 'http://www.pmsg.rj.gov.br/diario/{}.pdf'
    start_urls = ['http://www.pmsg.rj.gov.br/diario_oficial.php']

    def parse(self, response):
        date = datetime.date.today()
        end_date = datetime.date(1998, 2, 3)
        while date >= end_date:
            self.logger.info("got gazette for day %s", date)
            url = self.download_gazette_url.format(date.strftime('%Y_%m_%d'))
            is_extra_edition = False
            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                territory_id=self.TERRITORY_ID,
                power='executive',
                scraped_at=datetime.datetime.utcnow(),
            )
            date = date - datetime.timedelta(days=1)
