from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpRioDasPedrasSpider(DospGazetteSpider):
    TERRITORY_ID = "3544004"
    name = "sp_rio_das_pedras"
    code = 5143
    start_date = date(2017, 10, 11)
