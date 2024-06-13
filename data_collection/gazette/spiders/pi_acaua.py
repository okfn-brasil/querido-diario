import datetime as dt

from gazette.spiders.base.dioenet import BaseDioenetSpider


class PiAcauaSpider(BaseDioenetSpider):
    TERRITORY_ID = "2200053"
    name = "pi_acaua"
    start_date = dt.date(2021, 11, 5)
    end_date = dt.date.today()
    allowed_domains = ["plenussistemas.dioenet.com.br"]
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/acaua"
