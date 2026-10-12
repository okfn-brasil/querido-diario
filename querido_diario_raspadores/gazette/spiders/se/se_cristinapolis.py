from datetime import date

from gazette.spiders.base.agape import BaseAgapeSpider


class SeCristinapolisSpider(BaseAgapeSpider):
    TERRITORY_ID = "2801702"
    name = "se_cristinapolis"
    alias = "pmcristinapolis"
    start_date = date(2015, 3, 25)
