from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpIcemSpider(DospGazetteSpider):
    TERRITORY_ID = "3519808"
    name = "sp_icem"
    code = 4877
    start_date = date(2018, 5, 30)
