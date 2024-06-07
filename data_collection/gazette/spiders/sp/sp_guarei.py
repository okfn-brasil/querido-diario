from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpGuareiSpider(DospGazetteSpider):
    TERRITORY_ID = "3518503"
    name = "sp_guarei"
    code = 4860
    start_date = date(2019, 2, 6)
