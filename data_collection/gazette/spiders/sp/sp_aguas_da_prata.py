from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAguasDaPrataSpider(BaseDospSpider):
    TERRITORY_ID = "3500402"
    name = "sp_aguas_da_prata"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/aguas_da_prata"]
    start_date = date(2018, 8, 23)
