from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaSantaRitaDeCassiaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2928406"
    name = "ba_santa_rita_de_cassia"
    start_date = date(2021, 1, 4)
    state_city_url_part = "ba/santaritadecassia"
