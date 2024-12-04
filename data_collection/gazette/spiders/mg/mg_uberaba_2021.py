from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MgUberabaSpider(BaseDospSpider):
    TERRITORY_ID = "3170107"
    name = "mg_uberaba_2021"
    code = 2364
    start_date = date(2021, 9, 1)
