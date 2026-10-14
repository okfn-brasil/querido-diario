from datetime import date

from gazette.spiders.base.agape import BaseAgapeSpider


class SeCarmopolisSpider(BaseAgapeSpider):
    TERRITORY_ID = "2801504"
    name = "se_carmopolis"
    alias = "pmcarmopolis"
    start_date = date(2020, 4, 3)
