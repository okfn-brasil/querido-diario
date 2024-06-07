from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSaoJoseDoRioPardoSpider(DospGazetteSpider):
    TERRITORY_ID = "3549706"
    name = "sp_sao_jose_do_rio_pardo"
    code = 5206
    start_date = date(2018, 11, 7)
