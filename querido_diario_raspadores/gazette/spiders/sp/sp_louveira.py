from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpLouveiraSpider(BaseDospSpider):
    TERRITORY_ID = "3527306"
    name = "sp_louveira"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/louveira"]
    start_date = date(2019, 5, 15)
