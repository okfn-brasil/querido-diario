from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class RsQuatroIrmaosSpider(DospGazetteSpider):
    TERRITORY_ID = "4315313"
    name = "rs_quatro_irmaos"
    code = 4135
    start_date = date(2024, 5, 14)
