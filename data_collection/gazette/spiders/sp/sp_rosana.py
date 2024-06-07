from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpRosanaSpider(DospGazetteSpider):
    TERRITORY_ID = "3544251"
    name = "sp_rosana"
    code = 5147
    start_date = date(2019, 5, 4)
