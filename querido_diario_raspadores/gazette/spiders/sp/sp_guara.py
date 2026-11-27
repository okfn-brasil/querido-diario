from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpGuaraSpider(BaseDospSpider):
    TERRITORY_ID = "3517703"
    name = "sp_guara"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/guara"]
    start_date = date(2014, 12, 12)
