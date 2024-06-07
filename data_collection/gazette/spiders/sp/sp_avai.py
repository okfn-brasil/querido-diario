from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpAvaiSpider(DospGazetteSpider):
    TERRITORY_ID = "3504305"
    name = "sp_avai"
    code = 4698
    start_date = date(2017, 9, 18)
