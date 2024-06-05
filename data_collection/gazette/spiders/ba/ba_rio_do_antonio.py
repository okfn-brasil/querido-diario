from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaRioDoAntonioSpider(SaiGazetteSpider):
    TERRITORY_ID = "2926806"
    name = "ba_rio_do_antonio"
    allowed_domains = ["riodoantonio.ba.gov.br"]
    base_url = "https://www.riodoantonio.ba.gov.br"
    start_date = date(2009, 2, 9)
