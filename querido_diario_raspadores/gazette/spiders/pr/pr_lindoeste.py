from datetime import date

from gazette.spiders.base.eatos import BaseEatosSpider


class PrLindoesteSpider(BaseEatosSpider):
    TERRITORY_ID = "4113452"
    name = "pr_lindoeste"
    url_path = "lindoeste"
    start_date = date(2013, 12, 12)
