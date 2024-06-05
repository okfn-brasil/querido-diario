from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaOuricangasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2923308"
    name = "ba_ouricangas"
    allowed_domains = ["pmouricangas.ba.gov.br"]
    base_url = "https://www.pmouricangas.ba.gov.br"
    start_date = date(2010, 1, 14)
