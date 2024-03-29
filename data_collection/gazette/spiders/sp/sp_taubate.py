from datetime import date

from gazette.spiders.base.dioenet import DionetGazetteSpider


class SpTaubateSpider(DionetGazetteSpider):
    TERRITORY_ID = "3554102"
    name = "sp_taubate"
    start_date = date(2022, 12, 8)
