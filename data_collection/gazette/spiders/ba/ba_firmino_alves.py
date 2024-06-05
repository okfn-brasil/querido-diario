from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaFirminoAlvesSpider(SaiGazetteSpider):
    TERRITORY_ID = "2910909"
    name = "ba_firmino_alves"
    allowed_domains = ["firminoalves.ba.gov.br"]
    base_url = "https://www.firminoalves.ba.gov.br"
    start_date = date(2008, 12, 23)
