from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MsParanhosSpider(BaseDospSpider):
    TERRITORY_ID = "5006358"
    name = "ms_paranhos"
    code = 1521
    start_date = date(2023, 7, 13)
