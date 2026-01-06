from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class PrCarambeiSpider(BaseDospSpider):
    TERRITORY_ID = "4104659"
    name = "pr_carambei"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/carambei"]
    start_date = date(2022, 11, 9)
