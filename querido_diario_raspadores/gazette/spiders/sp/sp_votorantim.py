from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpVotorantimSpider(BaseInstarSpider):
    TERRITORY_ID = "3557006"
    name = "sp_votorantim"
    base_url = "https://www.votorantim.sp.gov.br/portal/diario-oficial"
    start_date = date(2018, 4, 20)
