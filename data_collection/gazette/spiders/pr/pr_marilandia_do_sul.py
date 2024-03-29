from datetime import date

from gazette.spiders.base.dioenet import DionetGazetteSpider


class PrMarilandiaDoSulSpider(DionetGazetteSpider):
    TERRITORY_ID = "4114906"
    name = "pr_marilandia_do_sul"
    start_date = date(2019, 12, 17)
