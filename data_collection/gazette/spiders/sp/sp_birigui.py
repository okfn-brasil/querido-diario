from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBiriguiSpider(BaseDospSpider):
    TERRITORY_ID = "3506508"
    name = "sp_birigui"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/birigui"]
    start_date = date(2016, 12, 28)
