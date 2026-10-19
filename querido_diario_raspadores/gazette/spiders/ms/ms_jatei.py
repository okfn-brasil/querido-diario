from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MsJateiSpider(BaseDospSpider):
    TERRITORY_ID = "5005103"
    name = "ms_jatei"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/jatei"]
    start_date = date(2017, 2, 13)
