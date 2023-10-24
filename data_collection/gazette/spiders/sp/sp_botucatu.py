from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpBotucatuSpider(BaseInstarSpider):
    TERRITORY_ID = "3507506"
    name = "sp_botucatu"
    allowed_domains = ["botucatu.sp.gov.br"]
    base_url = "https://www.botucatu.sp.gov.br/portal/diario-oficial"
    start_date = date(2000, 1, 6)
