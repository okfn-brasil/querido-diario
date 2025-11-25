import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class SpMacatubaSpider(BaseSigpubSpider):
    name = "sp_macatuba"
    TERRITORY_ID = "3528007"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/macatuba/"
    start_date = datetime.date(2018, 4, 25)
