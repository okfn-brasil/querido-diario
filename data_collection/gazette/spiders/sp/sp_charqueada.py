from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpCharqueadaSpider(BaseInstarSpider):
    TERRITORY_ID = "3511706"
    name = "sp_charqueada"
    allowed_domains = ["charqueada.sp.gov.br"]
    base_url = "https://www.charqueada.sp.gov.br/portal/diario-oficial"
    start_date = date(2009, 1, 9)
