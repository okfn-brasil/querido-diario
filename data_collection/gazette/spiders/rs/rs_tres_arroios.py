from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class RsTresArroiosSpider(BaseDospSpider):
    TERRITORY_ID = "4321634"
    name = "rs_tres_arroios"
    code = 4247
    start_date = date(2017, 4, 26)
