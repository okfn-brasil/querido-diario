from gazette.spiders.base.doem import DoemGazetteSpider
from datetime import date


class BaFlorestaAzulSpider(DoemGazetteSpider):
    TERRITORY_ID = "2911006"
    name = "ba_floresta_azul_2022"
    start_date = date(2017, 1, 2)
    state_city_url_part = "ba/florestaazul"
