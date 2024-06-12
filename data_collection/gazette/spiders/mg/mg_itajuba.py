from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class MgItajubaSpider(DospGazetteSpider):
    TERRITORY_ID = "3132404"
    name = "mg_itajuba"
    code = 1908
    start_date = date(2023, 5, 15)
