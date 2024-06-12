from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpAndradinaSpider(BaseInstarSpider):
    TERRITORY_ID = "3502101"
    name = "sp_andradina"
    allowed_domains = ["andradina.sp.gov.br"]
    base_url = "https://www.andradina.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 3, 3)
