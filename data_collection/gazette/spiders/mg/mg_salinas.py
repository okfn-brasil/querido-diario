from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgSalinasSpider(BaseInstarSpider):
    TERRITORY_ID = "3157005"
    name = "mg_salinas"
    allowed_domains = ["salinas.mg.gov.br"]
    base_url = "https://www.salinas.mg.gov.br/portal/diario-oficial"
    start_date = date(2017, 2, 1)
