from datetime import date

from gazette.spiders.base.eatos import BaseEatosSpider


class PrMedianeiraSpider(BaseEatosSpider):
    TERRITORY_ID = "4115804"
    name = "pr_medianeira"
    url_path = "medianeira"
    start_date = date(2010, 12, 29)
