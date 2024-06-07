from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpCatiguaSpider(DospGazetteSpider):
    TERRITORY_ID = "3511201"
    name = "sp_catigua"
    code = 4776
    start_date = date(2021, 4, 16)
