from datetime import date

from gazette.spiders.base.agape import BaseAgapeSpider


class SeBoquimSpider(BaseAgapeSpider):
    TERRITORY_ID = "2800670"
    name = "se_boquim"
    alias = "pmboquim"
    start_date = date(1999, 9, 30)
