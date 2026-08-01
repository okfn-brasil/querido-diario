from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpArapeiSpider(BaseInstarSpider):
    TERRITORY_ID = "3503158"
    name = "sp_arapei"
    base_url = "https://www.arapei.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 5, 27)
