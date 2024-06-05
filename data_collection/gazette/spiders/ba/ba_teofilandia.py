from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaTeofilandiaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2931509"
    name = "ba_teofilandia"
    allowed_domains = ["teofilandia.ba.gov.br"]
    base_url = "https://www.teofilandia.ba.gov.br"
    start_date = date(2010, 1, 7)
