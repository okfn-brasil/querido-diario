from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpGlicerioSpider(BaseInstarSpider):
    TERRITORY_ID = "3517109"
    name = "sp_glicerio"
    allowed_domains = ["glicerio.sp.gov.br"]
    start_date = date(2019, 1, 8)
    base_url = "https://www.glicerio.sp.gov.br/portal/diario-oficial/"
