from gazette.spiders.base import DoemGazetteSpider


class BaSantoEstevaoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2928802"
    name = "ba_santoestevao"
    state_city_url_part = "ba/santoestevao"
