from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpEliasFaustoSpider(DospGazetteSpider):
    TERRITORY_ID = "3514908"
    name = "sp_elias_fausto"
    code = 4814
    start_date = date(2018, 2, 9)
