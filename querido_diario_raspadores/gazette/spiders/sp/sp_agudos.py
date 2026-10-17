from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAgudosSpider(BaseDospSpider):
    TERRITORY_ID = "3500709"
    name = "sp_agudos"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/agudos"]
    start_date = date(2017, 6, 27)
