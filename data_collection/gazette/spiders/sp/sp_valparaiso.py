from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpValparaisoSpider(BaseInstarSpider):
    TERRITORY_ID = "3556305"
    name = "sp_valparaiso"
    allowed_domains = ["valparaiso.sp.gov.br"]
    base_url = "https://www.valparaiso.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 11, 19)
