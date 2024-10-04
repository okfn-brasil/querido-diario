from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaSantaRitaDeCassiaSpider(BaseDoemSpider):
    TERRITORY_ID = "2928406"
    name = "ba_santa_rita_de_cassia"
    state_city_url_part = "ba/santaritadecassia"
    start_date = date(2021, 1, 4)
