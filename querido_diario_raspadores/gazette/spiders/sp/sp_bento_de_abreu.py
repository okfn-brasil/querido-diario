from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBentoDeAbreuSpider(BaseDospSpider):
    TERRITORY_ID = "3506201"
    name = "sp_bento_de_abreu"
    start_urls = ["https://imprensaoficialmunicipal.com.br/bento_de_abreu"]
    start_date = date(2016, 6, 14)
