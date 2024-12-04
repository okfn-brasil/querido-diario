from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPlanaltoSpider(BaseInstarSpider):
    TERRITORY_ID = "3539608"
    name = "sp_planalto"
    allowed_domains = ["planalto.sp.gov.br"]
    base_url = "https://www.planalto.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 10, 10)
