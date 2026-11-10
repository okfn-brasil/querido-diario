from datetime import date

from gazette.spiders.base.eatos import BaseEatosSpider


class PrEntreRiosDoOesteSpider(BaseEatosSpider):
    TERRITORY_ID = "4107538"
    name = "pr_entre_rios_do_oeste"
    url_path = "entrerios"
    start_date = date(2013, 5, 2)
