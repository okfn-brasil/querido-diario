import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class GoGoianiraSpider(BaseSigpubSpider):
    name = "go_goianira"
    TERRITORY_ID = "5208806"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/agm/"
    start_date = datetime.date(2009, 1, 1)
