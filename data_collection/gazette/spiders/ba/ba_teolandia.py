from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaTeolandiaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2931608"
    name = "ba_teolandia"
    state_city_url_part = "ba/teolandia"
    start_date = date(2014, 1, 15)
