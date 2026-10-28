from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class PbMaltaSpider(BaseDioenetSpider):
    TERRITORY_ID = "2508802"
    name = "pb_malta"
    start_date = date(2022, 11, 9)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/malta"
    power = "executive_legislative"
