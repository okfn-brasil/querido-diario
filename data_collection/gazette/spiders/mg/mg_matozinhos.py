from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class MgMatozinhosSpider(DospGazetteSpider):
    TERRITORY_ID = "3141108"
    name = "mg_matozinhos"
    code = 2016
    start_date = date(2020, 4, 2)
