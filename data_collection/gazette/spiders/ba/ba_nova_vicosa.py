from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaNovaVicosaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2923001"
    name = "ba_nova_vicosa"
    allowed_domains = ["novavicosa.ba.gov.br"]
    base_url = "https://www.novavicosa.ba.gov.br"
    start_date = date(2007, 12, 17)
