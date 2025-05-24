from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class PrSaoJoaoDoTriunfoSpider(BaseInstarSpider):
    TERRITORY_ID = "4125100"
    name = "pr_sao_joao_do_triunfo"
    base_url = "https://www.sjtriunfo.pr.gov.br/portal/diario-oficial"
    start_date = date(2013, 4, 10)
