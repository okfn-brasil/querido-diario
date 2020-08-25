from dateparser import parse as parse_date
from datetime import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpFernandopolis(BaseGazetteSpider):
    MUNICIPALITY_ID = '3515509'
    name = 'sp_fernandopolis'
    start_urls = ['https://diariotransparente.com.br/publicacoes/frame/spfernandopolispm']

    def parse(self, response):
        IDX_EXTRA_EDITION_LI = 3
        list_pubs = response.css('div.row')
        for pub in list_pubs:
            link_date = pub.css('h3>a')
            date = link_date.css('::text').get()
            date = parse_date(date, languages=['pt']).date()
            link = response.urljoin(link_date.attrib['href'])
            is_extra_edition = pub.css('ul>li::text')[IDX_EXTRA_EDITION_LI].re_first('EXTRA') is None
            yield Gazette(
                date=date,
                file_urls=[link],
                is_extra_edition=is_extra_edition,
                municipality_id=self.MUNICIPALITY_ID,
                power="executive_legislature",
                scraped_at=datetime.utcnow(),
            )
