from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaJuazeiroSpider(DoemGazetteSpider):
    TERRITORY_ID = "2918407"
    name = "ba_juazeiro"
    start_date = date(2018, 1, 2)  # edition_number 1.135
    state_city_url_part = "ba/juazeiro"
