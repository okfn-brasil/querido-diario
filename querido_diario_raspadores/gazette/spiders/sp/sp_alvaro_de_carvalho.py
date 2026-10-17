from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAlvaroDeCarvalhoSpider(BaseDospSpider):
    TERRITORY_ID = "3501400"
    name = "sp_alvaro_de_carvalho"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/alvaro_de_carvalho"]
    start_date = date(2018, 4, 4)
