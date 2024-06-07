from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMonteAzulPaulistaSpider(DospGazetteSpider):
    TERRITORY_ID = "3531506"
    name = "sp_monte_azul_paulista"
    code = 5003
    start_date = date(2013, 10, 15)
