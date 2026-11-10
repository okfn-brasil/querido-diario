from datetime import date

from gazette.spiders.base.eatos import BaseEatosSpider


class PrVeraCruzDoOesteSpider(BaseEatosSpider):
    TERRITORY_ID = "4128559"
    name = "pr_vera_cruz_do_oeste"
    url_path = "veracruz"
    start_date = date(2011, 12, 1)
