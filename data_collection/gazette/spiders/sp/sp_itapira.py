from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpItapiraSpider(DospGazetteSpider):
    TERRITORY_ID = "3522604"
    name = "sp_itapira"
    code = 4909
    start_date = date(2011, 9, 16)
