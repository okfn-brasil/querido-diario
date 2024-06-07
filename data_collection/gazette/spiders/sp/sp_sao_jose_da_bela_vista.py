from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSaoJoseDaBelaVistaSpider(DospGazetteSpider):
    TERRITORY_ID = "3549508"
    name = "sp_sao_jose_da_bela_vista"
    code = 5204
    start_date = date(2021, 3, 8)
