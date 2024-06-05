from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCoribeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2909109"
    name = "ba_coribe"
    allowed_domains = ["coribe.ba.gov.br"]
    base_url = "https://www.coribe.ba.gov.br"
    start_date = date(2008, 9, 18)
