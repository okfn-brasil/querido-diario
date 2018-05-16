from dateparser import parse
import datetime as dt
from dateutil.rrule import rrule, MONTHLY

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpGuarulhosSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '3518800'
    name = 'sp_guarulhos'
    allowed_domains = ['guarulhos.sp.gov.br']
    urls = []
    starting_date = dt.date(2015, 1, 1)
    ending_date = dt.date.today()
    for date in rrule(MONTHLY, dtstart=starting_date, until=ending_date):
        url = "http://www.guarulhos.sp.gov.br/diario-oficial/index.php?mes={}&ano={}".format(
            date.month, date.year
        )
        urls.append(url)
    start_urls = urls

    def parse(self, response):
        """
        @url http://www.guarulhos.sp.gov.br/diario-oficial/index.php?mes=1&ano=2018
        @returns items 17 17
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """
        diarios = response.xpath('//div[contains(@id, "diario")]')
        items = []
        for diario in diarios:
            date = diario.xpath('.//h3/text()').extract_first()
            date = parse(date[-10:], languages=['pt']).date()
            is_extra_edition = False
            links = diario.xpath('.//a[contains(@href, ".pdf")]').xpath('@href')
            url = [response.urljoin(link) for link in links.extract()]
            power = 'executive'
            items.append(
                Gazette(
                    date=date,
                    file_urls=url,
                    is_extra_edition=is_extra_edition,
                    municipality_id=self.MUNICIPALITY_ID,
                    power=power,
                    scraped_at=dt.datetime.utcnow(),
                )
            )
        return items
