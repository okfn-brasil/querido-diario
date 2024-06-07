from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSantaCruzDaConceicaoSpider(DospGazetteSpider):
    TERRITORY_ID = "3546207"
    name = "sp_santa_cruz_da_conceicao"
    code = 5167
    start_date = date(2016, 10, 20)
