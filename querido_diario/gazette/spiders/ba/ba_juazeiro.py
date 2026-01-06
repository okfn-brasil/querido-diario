from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaJuazeiroSpider(BaseDoemSpider):
    TERRITORY_ID = "2918407"
    name = "ba_juazeiro"
    state_city_url_part = "ba/juazeiro"
    start_date = date(2013, 2, 1)
