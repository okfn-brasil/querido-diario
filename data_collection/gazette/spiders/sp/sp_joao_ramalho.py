from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpJoaoRamalhoSpider(BaseInstarSpider):
    TERRITORY_ID = "3525607"
    name = "sp_joao_ramalho"
    allowed_domains = ["joaoramalho.sp.gov.br"]
    base_url = "https://www.joaoramalho.sp.gov.br/portal/diario-oficial"
    start_date = date(2020, 3, 24)
