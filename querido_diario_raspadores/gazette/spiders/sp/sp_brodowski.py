from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBrodowskiSpider(BaseDospSpider):
    TERRITORY_ID = "3507803"
    name = "sp_brodowski"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/brodowski"]
    start_date = date(2017, 8, 8)
