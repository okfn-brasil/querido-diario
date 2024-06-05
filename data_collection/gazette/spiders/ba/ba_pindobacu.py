from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPindobacuSpider(SaiGazetteSpider):
    TERRITORY_ID = "2924603"
    name = "ba_pindobacu"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/pindobacu"
    start_date = date(2021, 1, 4)
