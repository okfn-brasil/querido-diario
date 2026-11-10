from datetime import date

from gazette.spiders.base.eatos import BaseEatosSpider


class PrMaripaSpider(BaseEatosSpider):
    TERRITORY_ID = "4115358"
    name = "pr_maripa"
    url_path = "maripa"
    start_date = date(2012, 9, 14)
