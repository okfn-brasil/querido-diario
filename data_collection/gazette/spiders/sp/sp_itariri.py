from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpItaririSpider(BaseInstarSpider):
    TERRITORY_ID = "3523305"
    name = "sp_itariri"
    allowed_domains = ["itariri.sp.gov.br"]
    base_url = "https://www.itariri.sp.gov.br/portal/diario-oficial"
    start_date = date(2023, 2, 24)
