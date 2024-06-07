from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpIarasSpider(DospGazetteSpider):
    TERRITORY_ID = "3519253"
    name = "sp_iaras"
    code = 4871
    start_date = date(2020, 5, 26)
