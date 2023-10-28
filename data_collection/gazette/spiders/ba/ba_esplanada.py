from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaEsplanadaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2910602"
    name = "ba_esplanada"
    start_date = date(2021, 1, 4)
    state_city_url_part = "ba/esplanada"
