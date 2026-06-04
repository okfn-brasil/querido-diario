import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class GoAcreunaSpider(BaseSigpubSpider):
    name = "go_acreuna"
    TERRITORY_ID = "5200134"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/agm/"
    start_date = datetime.date(2009, 1, 1)
