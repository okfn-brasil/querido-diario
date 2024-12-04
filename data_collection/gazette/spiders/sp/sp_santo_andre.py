from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpSantoAndreSpider(BaseInstarSpider):
    TERRITORY_ID = "3547809"
    name = "sp_santo_andre"
    allowed_domains = ["web.santoandre.sp.gov.br"]
    base_url = "https://web.santoandre.sp.gov.br/portal/diario-oficial"
    start_date = date(2010, 1, 5)
