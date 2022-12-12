import datetime as dt

from gazette.spiders.base.aplus import BaseAplusSpider


class MaPeritoroSpider(BaseAplusSpider):
    TERRITORY_ID = "2108454"
    name = "ma_peritoro"
    start_date = dt.date(2020, 1, 4)
    allowed_domains = ["peritoro.ma.gov.br"]
    url_base = "https://www.peritoro.ma.gov.br/diario/"
