from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaSantoEstevaoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2928802"
    name = "ba_santo_estevao"
    state_city_url_part = "ba/santoestevao"
    start_date = date(2017, 1, 6)
