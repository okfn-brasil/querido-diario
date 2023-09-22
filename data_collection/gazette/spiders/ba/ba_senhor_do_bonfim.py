from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaSenhorDoBonfimSpider(DoemGazetteSpider):
    TERRITORY_ID = "2930105"
    name = "ba_senhor_do_bonfim"
    start_date = date(2018, 1, 2)  # edition_number 1.503
    state_city_url_part = "ba/senhordobonfim"
