from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpEldoradoSpider(BaseInstarSpider):
    TERRITORY_ID = "3514809"
    name = "sp_eldorado"
    allowed_domains = ["eldorado.sp.gov.br"]
    base_url = "https://www.eldorado.sp.gov.br/portal/diario-oficial"
    start_date = date(2018, 12, 4)
