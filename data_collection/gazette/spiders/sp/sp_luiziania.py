from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpLuizianiaSpider(BaseInstarSpider):
    TERRITORY_ID = "3527702"
    name = "sp_luiziania"
    allowed_domains = ["luiziania.sp.gov.br"]
    base_url = "https://www.luiziania.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 4, 6)
