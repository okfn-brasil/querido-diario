from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaVarzeaNovaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2933158"
    name = "ba_varzea_nova"
    allowed_domains = ["varzeanova.ba.gov.br"]
    base_url = "https://www.varzeanova.ba.gov.br"
    start_date = date(2006, 3, 27)
