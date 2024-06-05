from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpSalesOliveiraSpider(BaseInstarSpider):
    TERRITORY_ID = "3544905"
    name = "sp_sales_oliveira"
    allowed_domains = ["salesoliveira.sp.gov.br"]
    base_url = "https://www.salesoliveira.sp.gov.br/portal/diario-oficial"
    start_date = date(2024, 1, 16)
