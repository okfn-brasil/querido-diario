from datetime import date

from gazette.spiders.base.agape import BaseAgapeSpider


class SeRibeiropolisSpider(BaseAgapeSpider):
    TERRITORY_ID = "2806008"
    name = "se_ribeiropolis"
    alias = "pmribeiropolis"
    start_date = date(2015, 1, 22)
