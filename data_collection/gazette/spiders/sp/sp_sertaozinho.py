from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSertaozinhoSpider(DospGazetteSpider):
    TERRITORY_ID = "3551702"
    name = "sp_sertaozinho"
    code = 5227
    start_date = date(2019, 8, 7)
