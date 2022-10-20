import datetime as dt

from gazette.spiders.base.aplus import BaseAplusSpider


class MaCodoSpider(BaseAplusSpider):
    TERRITORY_ID = "2103307"
    name = "ma_codo"
    start_date = dt.date(2020, 2, 17)
    allowed_domains = ["codo.ma.gov.br"]
    url_base = "https://www.codo.ma.gov.br/diario/"
