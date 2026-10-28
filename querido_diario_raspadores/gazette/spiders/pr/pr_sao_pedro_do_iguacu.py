from datetime import date

from gazette.spiders.base.dioenet import BaseDioenetSpider


class PrSaoPedroDoIguacuSpider(BaseDioenetSpider):
    TERRITORY_ID = "4125753"
    name = "pr_sao_pedro_do_iguacu"
    start_date = date(2021, 5, 31)
    end_date = date(2026, 5, 15)
    BASE_URL = "https://plenussistemas.dioenet.com.br/list/sao-pedro-do-iguacu"
    power = "executive_legislative"
