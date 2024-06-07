from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMairinqueSpider(DospGazetteSpider):
    TERRITORY_ID = "3528403"
    name = "sp_mairinque"
    code = 4970
    start_date = date(2024, 1, 19)
