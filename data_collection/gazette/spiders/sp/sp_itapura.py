from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpItapuraSpider(DospGazetteSpider):
    TERRITORY_ID = "3523008"
    name = "sp_itapura"
    code = 4914
    start_date = date(2018, 7, 11)
