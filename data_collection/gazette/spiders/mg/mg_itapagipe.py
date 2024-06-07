from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class MgItapagipeSpider(DospGazetteSpider):
    TERRITORY_ID = "3133402"
    name = "mg_itapagipe"
    code = 1918
    start_date = date(2021, 3, 8)
