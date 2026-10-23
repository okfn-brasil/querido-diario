from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpGarcaSpider(BaseDospSpider):
    TERRITORY_ID = "3516705"
    name = "sp_garca"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/garca"]
    start_date = date(2014, 8, 25)
