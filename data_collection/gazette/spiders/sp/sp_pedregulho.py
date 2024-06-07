from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPedregulhoSpider(DospGazetteSpider):
    TERRITORY_ID = "3537008"
    name = "sp_pedregulho"
    code = 5067
    start_date = date(2024, 1, 5)
