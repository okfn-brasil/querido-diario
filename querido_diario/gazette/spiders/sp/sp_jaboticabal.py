from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpJaboticabalSpider(BaseInstarSpider):
    TERRITORY_ID = "3524303"
    name = "sp_jaboticabal"
    base_url = "https://www.jaboticabal.sp.gov.br/portal/diario-oficial"
    start_date = date(2009, 8, 21)
