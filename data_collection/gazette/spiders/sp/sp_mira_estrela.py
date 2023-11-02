from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpMiraEstrelaSpider(BaseInstarSpider):
    TERRITORY_ID = "3530003"
    name = "sp_mira_estrela"
    allowed_domains = ["miraestrela.sp.gov.br"]
    base_url = "https://www.miraestrela.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 2, 16)
