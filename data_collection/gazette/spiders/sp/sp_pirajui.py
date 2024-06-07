from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPirajuiSpider(DospGazetteSpider):
    TERRITORY_ID = "3538907"
    name = "sp_pirajui"
    code = 5086
    start_date = date(2017, 4, 25)
