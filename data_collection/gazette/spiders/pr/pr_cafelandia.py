from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class PrCafelandiaSpider(DospGazetteSpider):
    TERRITORY_ID = "4103453"
    name = "pr_cafelandia"
    code = 4748
    start_date = date(2017, 6, 12)
