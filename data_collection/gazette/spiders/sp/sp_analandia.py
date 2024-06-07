from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpAnalandiaSpider(DospGazetteSpider):
    TERRITORY_ID = "3502002"
    name = "sp_analandia"
    code = 4671
    start_date = date(2022, 11, 11)
