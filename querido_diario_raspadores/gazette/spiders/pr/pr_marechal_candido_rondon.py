from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class PrMarechalCandidoRondonSpider(BaseDioenetSpider):
    TERRITORY_ID = "4114609"
    name = "pr_marechal_candido_rondon"
    start_date = date(2012, 6, 19)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/marechal-candido-rondon"
    power = "executive_legislative"
