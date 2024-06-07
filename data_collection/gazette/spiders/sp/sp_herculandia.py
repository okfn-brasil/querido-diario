from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpHerculandiaSpider(DospGazetteSpider):
    TERRITORY_ID = "3519006"
    name = "sp_herculandia"
    code = 4866
    start_date = date(2020, 1, 31)
