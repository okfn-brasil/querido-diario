from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class MgSacramentoSpider(BaseDioenetSpider):
    TERRITORY_ID = "3156908"
    name = "mg_sacramento"
    start_date = date(2019, 2, 26)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/sacramento"
    power = "executive_legislative"
