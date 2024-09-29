from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class RsMarauSpider(BaseDospSpider):
    TERRITORY_ID = "4311809"
    name = "rs_marau"
    code = 4049
    start_date = date(2017, 10, 10)
