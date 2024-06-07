from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSantaRitaDoPassaQuatroSpider(DospGazetteSpider):
    TERRITORY_ID = "3547502"
    name = "sp_santa_rita_do_passa_quatro"
    code = 5179
    start_date = date(2018, 1, 8)
