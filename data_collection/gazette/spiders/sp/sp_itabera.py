from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpItaberaSpider(DospGazetteSpider):
    TERRITORY_ID = "3521705"
    name = "sp_itabera"
    code = 4899
    start_date = date(2018, 10, 24)
