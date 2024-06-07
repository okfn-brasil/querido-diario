from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTorrinhaSpider(DospGazetteSpider):
    TERRITORY_ID = "3554706"
    name = "sp_torrinha"
    code = 5262
    start_date = date(2021, 6, 2)
