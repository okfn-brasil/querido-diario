from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MgUberabaSpider(BaseDospSpider):
    TERRITORY_ID = "3170107"
    name = "mg_uberaba_2021"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/uberaba"]
    start_date = date(2021, 9, 1)
