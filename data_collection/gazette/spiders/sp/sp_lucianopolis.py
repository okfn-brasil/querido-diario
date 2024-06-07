from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpLucianopolisSpider(DospGazetteSpider):
    TERRITORY_ID = "3527504"
    name = "sp_lucianopolis"
    code = 4961
    start_date = date(2022, 11, 1)
