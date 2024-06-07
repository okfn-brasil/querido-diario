from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpVargemGrandePaulistaSpider(DospGazetteSpider):
    TERRITORY_ID = "3556453"
    name = "sp_vargem_grande_paulista"
    code = 5284
    start_date = date(2019, 6, 7)
