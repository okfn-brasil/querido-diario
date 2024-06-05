from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaNovaCanaaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2922706"
    name = "ba_nova_canaa"
    allowed_domains = ["novacanaa.ba.gov.br"]
    base_url = "https://www.novacanaa.ba.gov.br"
    start_date = date(2007, 1, 15)
