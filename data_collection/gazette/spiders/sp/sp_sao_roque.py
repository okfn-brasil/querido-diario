from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpSaoRoqueSpider(BaseInstarSpider):
    TERRITORY_ID = "3550605"
    name = "sp_sao_roque"
    allowed_domains = ["saoroque.sp.gov.br"]
    base_url = "https://www.saoroque.sp.gov.br/portal/diario-oficial"
    start_date = date(2020, 5, 8)
