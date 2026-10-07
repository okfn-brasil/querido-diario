import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class GoAguasLindasDeGoiasSpider(BaseSigpubSpider):
    name = "go_aguas_lindas_de_goias"
    TERRITORY_ID = "5200258"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/agm/"
    start_date = datetime.date(2009, 1, 1)
