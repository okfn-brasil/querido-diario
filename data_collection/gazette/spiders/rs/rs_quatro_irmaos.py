from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class RsQuatroIrmaosSpider(BaseDospSpider):
    TERRITORY_ID = "4315313"
    name = "rs_quatro_irmaos"
    code = 4135
    start_date = date(2024, 5, 14)
