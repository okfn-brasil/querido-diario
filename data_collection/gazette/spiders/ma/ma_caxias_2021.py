import datetime as dt

from gazette.spiders.base.aplus import BaseAplusSpider


class MaCaxiasSpider(BaseAplusSpider):
    TERRITORY_ID = "2103000"
    name = "ma_caxias_2021"
    start_date = dt.date(2021, 8, 6)
    BASE_URL = "https://dom.caxias.ma.gov.br/diario/"
