from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaRibeiraoDoLargoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2926657"
    name = "ba_ribeirao_do_largo"
    allowed_domains = ["ribeiraodolargo.ba.gov.br"]
    base_url = "https://www.ribeiraodolargo.ba.gov.br"
    start_date = date(2013, 1, 2)
