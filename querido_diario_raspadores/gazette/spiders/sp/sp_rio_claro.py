from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpRioClaroSpider(BaseDospSpider):
    TERRITORY_ID = "3543907"
    name = "sp_rio_claro"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/rio_claro"]
    start_date = date(2006, 5, 23)
