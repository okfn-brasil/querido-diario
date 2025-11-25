from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpVotuporangaSpider(BaseDospSpider):
    TERRITORY_ID = "3557105"
    name = "sp_votuporanga"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/votuporanga"]
    start_date = date(2015, 10, 5)
