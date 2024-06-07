from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpRioGrandeDaSerraSpider(DospGazetteSpider):
    TERRITORY_ID = "3544103"
    name = "sp_rio_grande_da_serra"
    code = 5144
    start_date = date(2022, 8, 4)
