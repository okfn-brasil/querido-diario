from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class RsSaoFranciscoDePaulaSpider(BaseInstarSpider):
    TERRITORY_ID = "4318200"
    name = "rs_sao_francisco_de_paula"
    base_url = "http://www.saofranciscodepaula.rs.gov.br/portal/diario-oficial"
    start_date = date(2023, 8, 31)
