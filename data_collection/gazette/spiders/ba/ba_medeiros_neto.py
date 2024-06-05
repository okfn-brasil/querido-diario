from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMedeirosNetoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2921104"
    name = "ba_medeiros_neto"
    allowed_domains = ["medeirosneto.ba.gov.br"]
    base_url = "https://www.medeirosneto.ba.gov.br"
    start_date = date(2008, 4, 1)
