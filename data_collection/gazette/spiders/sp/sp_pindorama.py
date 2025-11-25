from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPindoramaSpider(BaseInstarSpider):
    TERRITORY_ID = "3538105"
    name = "sp_pindorama"
    base_url = "https://www.pindorama.sp.gov.br/portal/diario-oficial"
    start_date = date(2022, 4, 29)
