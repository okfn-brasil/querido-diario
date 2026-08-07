import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class GoCristalinaSpider(BaseSigpubSpider):
    name = "go_cristalina"
    TERRITORY_ID = "5206206"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/agm/"
    start_date = datetime.date(2009, 1, 1)
