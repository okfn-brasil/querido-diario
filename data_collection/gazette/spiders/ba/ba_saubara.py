from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSaubaraSpider(SaiGazetteSpider):
    TERRITORY_ID = "2929750"
    name = "ba_saubara"
    allowed_domains = ["saubara.ba.gov.br"]
    base_url = "https://www.saubara.ba.gov.br"
    start_date = date(2009, 2, 12)
