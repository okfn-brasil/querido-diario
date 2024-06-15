from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpTapiraiSpider(BaseInstarSpider):
    TERRITORY_ID = "3553500"
    name = "sp_tapirai"
    allowed_domains = ["tapirai.sp.gov.br"]
    base_url = "https://www.tapirai.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 9, 3)
