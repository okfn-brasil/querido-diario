from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpCatanduvaSpider(BaseDospSpider):
    TERRITORY_ID = "3511102"
    name = "sp_catanduva"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/catanduva"]
    start_date = date(2016, 3, 18)
