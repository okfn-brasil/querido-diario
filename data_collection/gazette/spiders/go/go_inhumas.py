import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class GoInhumasSpider(BaseSigpubSpider):
    name = "go_inhumas"
    TERRITORY_ID = "5210000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/agm/"
    start_date = datetime.date(2009, 1, 1)
