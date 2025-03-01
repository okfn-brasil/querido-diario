from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpMonteiroLobatoSpider(BaseDospSpider):
    TERRITORY_ID = "3531704"
    name = "sp_monteiro_lobato"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/monteiro_lobato"]
    start_date = date(2020, 11, 26)
