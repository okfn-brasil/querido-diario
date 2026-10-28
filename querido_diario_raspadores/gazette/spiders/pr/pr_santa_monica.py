from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class PrSantaMonicaSpider(BaseDioenetSpider):
    TERRITORY_ID = "4123956"
    name = "pr_santa_monica"
    start_date = date(2020, 4, 17)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/santa-monica"
    power = "executive_legislative"
