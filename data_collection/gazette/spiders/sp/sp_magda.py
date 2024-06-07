from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMagdaSpider(DospGazetteSpider):
    TERRITORY_ID = "3528304"
    name = "sp_magda"
    code = 4969
    start_date = date(2018, 7, 17)
