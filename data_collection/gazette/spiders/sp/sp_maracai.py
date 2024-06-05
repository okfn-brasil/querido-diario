from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpMaracaiSpider(BaseInstarSpider):
    TERRITORY_ID = "3528809"
    name = "sp_maracai"
    allowed_domains = ["maracai.sp.gov.br"]
    base_url = "https://www.maracai.sp.gov.br/portal/diario-oficial"
    start_date = date(2017, 8, 8)
