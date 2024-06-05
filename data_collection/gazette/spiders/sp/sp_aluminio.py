from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpAluminioSpider(BaseInstarSpider):
    TERRITORY_ID = "3501152"
    name = "sp_aluminio"
    allowed_domains = ["aluminio.sp.gov.br"]
    base_url = "https://www.aluminio.sp.gov.br/portal/diario-oficial"
    start_date = date(2013, 1, 31)
