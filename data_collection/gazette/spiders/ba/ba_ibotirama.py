from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIbotiramaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2913200"
    name = "ba_ibotirama"
    allowed_domains = ["ibotirama.ba.gov.br"]
    base_url = "https://www.ibotirama.ba.gov.br"
    start_date = date(2008, 1, 9)
