from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMilagresSpider(SaiGazetteSpider):
    TERRITORY_ID = "2921302"
    name = "ba_milagres"
    allowed_domains = ["milagres.ba.gov.br"]
    base_url = "https://www.milagres.ba.gov.br"
    start_date = date(2009, 8, 11)
