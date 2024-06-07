from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpIndiaporaSpider(DospGazetteSpider):
    TERRITORY_ID = "3520707"
    name = "sp_indiapora"
    code = 4888
    start_date = date(2015, 12, 24)
