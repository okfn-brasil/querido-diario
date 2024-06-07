from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class BaIbirataiaSpider(DospGazetteSpider):
    TERRITORY_ID = "2912905"
    name = "ba_ibirataia"
    code = 356
    start_date = date(2022, 5, 2)
