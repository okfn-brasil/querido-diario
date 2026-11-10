from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgCongonhasDoNorteSpider(BaseInstarSpider):
    TERRITORY_ID = "3118106"
    name = "mg_congonhas_do_norte"
    base_url = "https://www.congonhasdonorte.mg.gov.br/portal/diario-oficial"
    start_date = date(2024, 1, 10)
