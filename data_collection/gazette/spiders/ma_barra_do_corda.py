import datetime as dt

from gazette.spiders.base.dioenet import BaseDioenetSpider


class MaBarradoCordaSpider(BaseDioenetSpider):
    TERRITORY_ID = "2101608"
    name = "ma_barra_do_corda"
    start_date = dt.date(2021, 3, 5)
    end_date = dt.date.today()
    allowed_domains = ["plenussistemas.dioenet.com.br"]
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/barra-do-corda"
