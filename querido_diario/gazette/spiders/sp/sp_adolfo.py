from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAdolfoSpider(BaseDospSpider):
    TERRITORY_ID = "3500204"
    name = "sp_adolfo"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/adolfo"]
    start_date = date(2015, 5, 14)
