from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpIbitingaSpider(BaseInstarSpider):
    TERRITORY_ID = "3519600"
    name = "sp_ibitinga"
    allowed_domains = ["ibitinga.instarbr.com.br"]
    base_url = "https://www.ibitinga.instarbr.com.br/portal/diario-oficial"
    start_date = date(2019, 4, 30)
