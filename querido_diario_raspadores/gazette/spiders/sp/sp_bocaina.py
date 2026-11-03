from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBocainaSpider(BaseDospSpider):
    TERRITORY_ID = "3506805"
    name = "sp_bocaina"
    start_urls = ["https://imprensaoficialmunicipal.com.br/bocaina"]
    start_date = date(2018, 7, 23)
