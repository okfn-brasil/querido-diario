from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpLouveiraSpider(DospGazetteSpider):
    TERRITORY_ID = "3527306"
    name = "sp_louveira"
    code = 4959
    start_date = date(2019, 5, 15)
