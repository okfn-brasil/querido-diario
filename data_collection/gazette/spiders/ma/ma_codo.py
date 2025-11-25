import datetime as dt

from gazette.spiders.base.aplus import BaseAplusSpider


class MaCodoSpider(BaseAplusSpider):
    TERRITORY_ID = "2103307"
    name = "ma_codo"
    start_date = dt.date(2020, 2, 17)
    BASE_URL = "https://www.codo.ma.gov.br/diario/"
