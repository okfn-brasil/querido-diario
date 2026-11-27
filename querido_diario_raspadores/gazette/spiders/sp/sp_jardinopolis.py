from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpJardinopolisSpider(BaseDospSpider):
    TERRITORY_ID = "3525102"
    name = "sp_jardinopolis"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/jardinopolis"]
    start_date = date(2020, 3, 11)
