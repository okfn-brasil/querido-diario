from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpMorroAgudoSpider(BaseDospSpider):
    TERRITORY_ID = "3531902"
    name = "sp_morro_agudo"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/morro_agudo"]
    start_date = date(2017, 1, 24)
