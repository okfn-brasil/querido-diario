from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class PrPrimeiroDeMaioSpider(BaseInstarSpider):
    TERRITORY_ID = "4120507"
    name = "pr_primeiro_de_maio"
    allowed_domains = ["primeirodemaio.pr.gov.br"]
    base_url = "https://www.primeirodemaio.pr.gov.br/portal/diario-oficial"
    start_date = date(2022, 4, 14)
