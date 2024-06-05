from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCaraibasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2906899"
    name = "ba_caraibas"
    allowed_domains = ["caraibas.ba.gov.br"]
    base_url = "https://www.caraibas.ba.gov.br"
    start_date = date(2009, 1, 20)
