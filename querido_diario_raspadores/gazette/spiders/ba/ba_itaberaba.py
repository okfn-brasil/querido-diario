from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaItaberabaSpider(BaseDoemSpider):
    TERRITORY_ID = "2914703"
    name = "ba_itaberaba"
    state_city_url_part = "ba/itaberaba"
    start_date = date(2022, 7, 4)
