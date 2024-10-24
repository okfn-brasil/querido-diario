from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MsJateiSpider(BaseDospSpider):
    TERRITORY_ID = "5005103"
    name = "ms_jatei"
    code = 1508
    start_date = date(2023, 12, 12)
