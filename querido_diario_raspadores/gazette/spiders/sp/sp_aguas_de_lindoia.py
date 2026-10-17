from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAguasDeLindoiaSpider(BaseDospSpider):
    TERRITORY_ID = "3500501"
    name = "sp_aguas_de_lindoia"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/aguas_de_lindoia"]
    start_date = date(2020, 1, 31)
