from datetime import date

from gazette.spiders.base.eatos import BaseEatosSpider


class PrMatelandiaSpider(BaseEatosSpider):
    TERRITORY_ID = "4115606"
    name = "pr_matelandia"
    url_path = "matelandia"
    start_date = date(2011, 1, 27)
