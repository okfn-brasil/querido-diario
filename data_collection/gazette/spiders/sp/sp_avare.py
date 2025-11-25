from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAvareSpider(BaseDospSpider):
    TERRITORY_ID = "3504503"
    name = "sp_avare"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/avare"]
    start_date = date(2018, 10, 3)
