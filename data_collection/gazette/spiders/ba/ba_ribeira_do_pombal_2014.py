from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaRibeiraDoPombalSpider(DoemGazetteSpider):
    TERRITORY_ID = "2926608"
    name = "ba_ribeira_do_pombal_2014"
    state_city_url_part = "ba/ribeiradopombal"
    start_date = date(2014, 1, 16)
