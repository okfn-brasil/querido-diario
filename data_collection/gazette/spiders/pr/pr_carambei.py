from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class PrCarambeiSpider(DospGazetteSpider):
    TERRITORY_ID = "4104659"
    name = "pr_carambei"
    code = 2826
    start_date = date(2022, 11, 9)
