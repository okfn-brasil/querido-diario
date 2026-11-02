from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBarraBonitaSpider(BaseDospSpider):
    TERRITORY_ID = "3505302"
    name = "sp_barra_bonita"
    start_urls = ["https://imprensaoficialmunicipal.com.br/barra_bonita"]
    start_date = date(2021, 5, 18)
