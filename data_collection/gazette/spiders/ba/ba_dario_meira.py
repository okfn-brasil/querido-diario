from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaDarioMeiraSpider(SaiGazetteSpider):
    TERRITORY_ID = "2910008"
    name = "ba_dario_meira"
    allowed_domains = ["dariomeira.ba.gov.br"]
    base_url = "https://www.dariomeira.ba.gov.br"
    start_date = date(2007, 1, 4)
