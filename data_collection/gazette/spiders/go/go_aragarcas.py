import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class GoAragarcasSpider(BaseSigpubSpider):
    name = "go_aragarcas"
    TERRITORY_ID = "5201702"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/agm/"
    start_date = datetime.date(2009, 1, 1)
