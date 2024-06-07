from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTacibaSpider(DospGazetteSpider):
    TERRITORY_ID = "3552908"
    name = "sp_taciba"
    code = 5240
    start_date = date(2018, 7, 10)
