from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaAlagoinhasSpider(DoemGazetteSpider):
    TERRITORY_ID = "2900702"
    name = "ba_alagoinhas"
    start_date = date(2018, 1, 2)  # edition_number 1.950
    state_city_url_part = "ba/alagoinhas"
