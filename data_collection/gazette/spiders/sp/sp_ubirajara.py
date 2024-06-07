from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpUbirajaraSpider(DospGazetteSpider):
    TERRITORY_ID = "3555505"
    name = "sp_ubirajara"
    code = 5273
    start_date = date(2018, 4, 13)
