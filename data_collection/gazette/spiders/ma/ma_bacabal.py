import datetime as dt

from gazette.spiders.base.aplus import BaseAplusSpider


class MaBacabalSpider(BaseAplusSpider):
    TERRITORY_ID = "2101202"
    name = "ma_bacabal"
    start_date = dt.date(2016, 5, 13)
    allowed_domains = ["bacabal.ma.gov.br"]
    url_base = "https://www.bacabal.ma.gov.br/diario/"
