from dateparser import parse
import datetime as dt
import pandas as pd

import scrapy

from gazette.items import Gazette


class SpGuarulhosSpider(scrapy.Spider):
    MUNICIPALITY_ID = ' 3518800'
    name = 'sp_guarulhos'
    allowed_domains = ['guarulhos.sp.gov.br']

    urls = []

    start_date = '2015-01-01'
    today = dt.date.today()

    dates = pd.date_range(start_date, today, freq='MS')

    for date in dates:
            url = "http://www.guarulhos.sp.gov.br/diario-oficial/index.php?mes={}&ano={}".format(date.month, date.year)

            urls.append(url)


    start_urls = urls

    def parse(self, response):
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
                        scraped_at=dt.datetime.utcnow(),
                        power=power,
                    )
                )
        
        return items