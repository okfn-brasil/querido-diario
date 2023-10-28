from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPiedadeSpider(BaseInstarSpider):
    TERRITORY_ID = "3537800"
    name = "sp_piedade"
    allowed_domains = ["piedade.sp.gov.br"]
    base_url = "https://www.piedade.sp.gov.br/portal/diario-oficial"
    start_date = date(2018, 10, 11)
