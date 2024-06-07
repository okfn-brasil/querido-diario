from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMendoncaSpider(DospGazetteSpider):
    TERRITORY_ID = "3529500"
    name = "sp_mendonca"
    code = 4982
    start_date = date(2023, 1, 25)
