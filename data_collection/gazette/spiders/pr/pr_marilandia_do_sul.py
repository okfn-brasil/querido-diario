from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class PrMarilandiaDoSulSpider(BaseDioenetSpider):
    TERRITORY_ID = "4114906"
    name = "pr_marilandia_do_sul"
    start_date = date(2019, 12, 17)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/marilandia-do-sul"
    power = "executive_legislative"
