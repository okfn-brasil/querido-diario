from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpGaliaSpider(DospGazetteSpider):
    TERRITORY_ID = "3516606"
    name = "sp_galia"
    code = 4840
    start_date = date(2018, 3, 1)
