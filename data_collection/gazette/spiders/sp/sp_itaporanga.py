from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpItaporangaSpider(BaseInstarSpider):
    TERRITORY_ID = "3522802"
    name = "sp_itaporanga"
    allowed_domains = ["itaporanga.sp.gov.br"]
    base_url = "https://www.itaporanga.sp.gov.br/portal/diario-oficial"
    start_date = date(2011, 6, 7)
