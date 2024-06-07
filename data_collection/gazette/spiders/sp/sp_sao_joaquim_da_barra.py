from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSaoJoaquimDaBarraSpider(DospGazetteSpider):
    TERRITORY_ID = "3549409"
    name = "sp_sao_joaquim_da_barra"
    code = 5203
    start_date = date(2017, 5, 26)
