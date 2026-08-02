from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class SpTaubateSpider(BaseDioenetSpider):
    TERRITORY_ID = "3554102"
    name = "sp_taubate"
    start_date = date(2022, 12, 8)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/taubate"
    power = "executive_legislative"
