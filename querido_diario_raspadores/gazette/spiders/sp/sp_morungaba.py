from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpMorungabaSpider(BaseDospSpider):
    TERRITORY_ID = "3532009"
    name = "sp_morungaba"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/morungaba"]
    start_date = date(2017, 8, 8)
