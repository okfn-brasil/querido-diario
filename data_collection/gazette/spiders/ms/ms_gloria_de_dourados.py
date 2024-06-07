from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class MsGloriaDeDouradosSpider(DospGazetteSpider):
    TERRITORY_ID = "5004007"
    name = "ms_gloria_de_dourados"
    code = 1498
    start_date = date(2023, 11, 7)
