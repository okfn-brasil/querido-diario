from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpVargemGrandeDoSulSpider(DospGazetteSpider):
    TERRITORY_ID = "3556404"
    name = "sp_vargem_grande_do_sul"
    code = 5283
    start_date = date(2018, 9, 6)
