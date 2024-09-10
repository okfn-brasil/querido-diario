from datetime import date

from gazette.spiders.base.dioenet import DioenetGazetteSpider


class RjNovaFriburgoSpider(DioenetGazetteSpider):
    TERRITORY_ID = "3303401"
    name = "rj_nova_friburgo"
    start_date = date(2019, 10, 17)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/nova-friburgo"
    power = "executive_legislative"
