from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class PeCabroboSpider(BaseDospSpider):
    TERRITORY_ID = "2603009"
    name = "pe_cabrobo"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/cabrobo"]
    start_date = date(2019, 4, 8)
