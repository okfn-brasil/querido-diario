from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class MgSantanaDoGarambeuSpider(BaseDioenetSpider):
    TERRITORY_ID = "3158706"
    name = "mg_santana_do_garambeu"
    start_date = date(2022, 9, 22)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/santana-do-garambeu"
    power = "executive_legislative"
