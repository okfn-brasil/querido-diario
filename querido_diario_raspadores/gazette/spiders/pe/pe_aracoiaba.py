from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class PeAracoiabaSpider(BaseDospSpider):
    TERRITORY_ID = "2601052"
    name = "pe_aracoiaba"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/aracoiaba"]
    start_date = date(2017, 7, 6)
