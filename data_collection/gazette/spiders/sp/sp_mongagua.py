from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMongaguaSpider(DospGazetteSpider):
    TERRITORY_ID = "3531100"
    name = "sp_mongagua"
    code = 4999
    start_date = date(2017, 8, 24)
