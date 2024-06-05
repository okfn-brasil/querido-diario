from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSerraDouradaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2930303"
    name = "ba_serra_dourada"
    allowed_domains = ["serradourada.ba.gov.br"]
    base_url = "https://www.serradourada.ba.gov.br"
    start_date = date(2007, 4, 3)
