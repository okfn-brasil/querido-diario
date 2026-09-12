import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class GoCacuSpider(BaseSigpubSpider):
    name = "go_cacu"
    TERRITORY_ID = "5204300"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/agm/"
    start_date = datetime.date(2009, 1, 1)
