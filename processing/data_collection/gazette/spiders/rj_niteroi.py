import datetime as dt

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjNiteroiSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '3303302'
    name = 'rj_niteroi'
    allowed_domains = ['niteroi.rj.gov.br']
    start_urls = ['http://www.niteroi.rj.gov.br']
    download_url = 'http://www.niteroi.rj.gov.br/downloads/do/{}/{}/{:02d}'
    month_names = ['01_Jan', '02_Fev', '03_Mar', '04_Abr', '05_Mai',
                   '06_Jun', '07_Jul', '08_Ago', '09_Set', '10_Out', '11_Nov', '12_Dez']

    def parse(self, response):
        """
        @url http://www.niteroi.rj.gov.br
        @returns items 1
        @scrapes date file_urls municipality_id power scraped_at
        """
        start_date = dt.date(2003, 7, 1)
        parsing_date = dt.date.today()
        while parsing_date >= start_date:
            month = self.month_names[parsing_date.month - 1]
            url = self.download_url.format(
                parsing_date.year, month, parsing_date.day)
            yield Gazette(
                date=parsing_date,
                file_urls=[url],
                municipality_id=self.MUNICIPALITY_ID,
                power='executive_legislature',
                scraped_at=dt.datetime.utcnow()
            )
            parsing_date = parsing_date - dt.timedelta(days=1)
