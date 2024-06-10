from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSaoBernardoDoCampoSpider(DospGazetteSpider):
    TERRITORY_ID = "3548708"
    name = "sp_sao_bernardo_do_campo"
    code = 5195
    start_date = date(2017, 5, 12)
