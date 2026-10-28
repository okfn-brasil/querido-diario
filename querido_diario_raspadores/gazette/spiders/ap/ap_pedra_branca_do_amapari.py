from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class ApPedraBrancaDoAmapariSpider(BaseDioenetSpider):
    TERRITORY_ID = "1600154"
    name = "ap_pedra_branca_do_amapari"
    start_date = date(2020, 3, 9)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/pedra-branca-do-amapari"
    power = "executive_legislative"
