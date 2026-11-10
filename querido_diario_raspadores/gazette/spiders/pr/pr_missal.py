from datetime import date

from gazette.spiders.base.eatos import BaseEatosSpider


class PrMissalSpider(BaseEatosSpider):
    TERRITORY_ID = "4116059"
    name = "pr_missal"
    url_path = "missal"
    start_date = date(2011, 7, 14)
