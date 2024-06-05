from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSantaTeresinhaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2928505"
    name = "ba_santa_teresinha"
    allowed_domains = ["santateresinha.ba.gov.br"]
    base_url = "https://www.santateresinha.ba.gov.br"
    start_date = date(2008, 4, 4)
