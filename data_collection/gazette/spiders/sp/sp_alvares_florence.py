from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpCajuruSpider(BaseInstarSpider):
    TERRITORY_ID = "3501202"
    name = "sp_alvares_florence"
    allowed_domains = ["alvaresflorence.sp.gov.br"]
    base_url = "https://www.alvaresflorence.sp.gov.br/portal/diario-oficial"
    start_date = date(2013, 3, 13)
