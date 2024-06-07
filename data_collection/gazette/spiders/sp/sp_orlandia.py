from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpOrlandiaSpider(DospGazetteSpider):
    TERRITORY_ID = "3534302"
    name = "sp_orlandia"
    code = 5037
    start_date = date(2021, 12, 1)
