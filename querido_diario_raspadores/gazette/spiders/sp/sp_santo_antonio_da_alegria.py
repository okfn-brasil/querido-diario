from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class SpSantoAntonioDaAlegriaSpider(BaseDioenetSpider):
    TERRITORY_ID = "3547908"
    name = "sp_santo_antonio_da_alegria"
    start_date = date(2022, 11, 17)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/santo-antonio-da-alegria"
    power = "executive_legislative"
