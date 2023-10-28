from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaSantoAmaroSpider(DoemGazetteSpider):
    TERRITORY_ID = "2928604"
    name = "ba_santo_amaro_2012"
    state_city_url_part = "ba/santoamaro"
    start_date = date(2012, 12, 6)
