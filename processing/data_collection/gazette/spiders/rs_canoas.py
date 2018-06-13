import json
from datetime import date, datetime, timedelta

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RsCanoasSpider(BaseGazetteSpider):
    TERRITORY_ID = '4304606'
    name = 'rs_canoas'
    START_DATE = date(2018, 5, 29)
    BASE_URL = 'https://sistemas.canoas.rs.gov.br/domc/api/'

    def start_requests(self):
        today = date.today()
        day = self.START_DATE
        while day < today:
            url = '{}public/diary-by-day?day={}'.format(
                self.BASE_URL, day.strftime('%d/%m/%Y'))
            yield scrapy.Request(url)
            day = day + timedelta(days=1)

    def parse(self, response):
        """
        @url https://sistemas.canoas.rs.gov.br/domc/api/public/diary-by-day?day=08/06/2018  # noqa
        @returns items 3 3
        @scrapes date file_urls is_extra_edition territory_id power scraped_at
        """
        data = json.loads(response.body_as_unicode())
        items = []

        for edition in data['editions']:
            file_url = '{}edition-file/{}'.format(self.BASE_URL, edition['id'])
            is_extra_edition = edition['type'] == 'C'

            items.append(
                Gazette(
                    date=data['day'],
                    file_urls=[file_url],
                    is_extra_edition=is_extra_edition,
                    territory_id=self.TERRITORY_ID,
                    power='executive',
                    scraped_at=datetime.utcnow(),
                )
            )
        return items
