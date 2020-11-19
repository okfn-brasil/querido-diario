from gazette.spiders.base import DoemGazetteSpider


class BaRibeiraDoPombalSpider(DoemGazetteSpider):
    TERRITORY_ID = "2926608"
    name = "ba_ribeiradopombal"
    state_city_url_part = "ba/ribeiradopombal"
