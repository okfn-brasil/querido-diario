from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpSarutaiaSpider(BaseInstarSpider):
    TERRITORY_ID = "3551207"
    name = "sp_sarutaia"
    allowed_domains = ["sarutaia.sp.gov.br"]
    start_date = date(2020, 3, 27)
    start_urls = "https://www.sarutaia.sp.gov.br/portal/diario-oficial"
