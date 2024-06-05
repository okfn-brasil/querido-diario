from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItajuipeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2915502"
    name = "ba_itajuipe"
    allowed_domains = ["itajuipe.ba.gov.br"]
    base_url = "https://www.itajuipe.ba.gov.br"
    start_date = date(2007, 1, 29)
