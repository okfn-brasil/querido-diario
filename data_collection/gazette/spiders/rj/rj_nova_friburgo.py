from datetime import date

from gazette.spiders.base.dioenet import DionetGazetteSpider


class RjNovaFriburgoSpider(DionetGazetteSpider):
    TERRITORY_ID = "3303401"
    name = "rj_nova_friburgo"
    start_date = date(2019, 10, 17)
