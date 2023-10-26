from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpSantaMariaDaSerraSpider(BaseInstarSpider):
    TERRITORY_ID = "3547007"
    name = "sp_santa_maria_da_serra"
    allowed_domains = ["santamariadaserra.sp.gov.br"]
    base_url = "https://www.santamariadaserra.sp.gov.br/portal/diario-oficial"
    start_date = date(2022, 3, 16)
