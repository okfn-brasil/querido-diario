from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBastosSpider(DospGazetteSpider):
    TERRITORY_ID = "3505807"
    name = "sp_bastos"
    code = 4714
    start_date = date(2022, 3, 17)
