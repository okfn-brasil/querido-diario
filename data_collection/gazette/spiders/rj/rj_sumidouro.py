from datetime import date

from gazette.spiders.base.dioenet import DioenetGazetteSpider


class RjSumidouroSpider(DioenetGazetteSpider):
    TERRITORY_ID = "3305703"
    name = "rj_sumidouro"
    start_date = date(2021, 7, 26)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/sumidouro"
    power = "executive_legislative"
