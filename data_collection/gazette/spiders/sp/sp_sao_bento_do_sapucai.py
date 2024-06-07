from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSaoBentoDoSapucaiSpider(DospGazetteSpider):
    TERRITORY_ID = "3548609"
    name = "sp_sao_bento_do_sapucai"
    code = 5194
    start_date = date(2021, 4, 7)
