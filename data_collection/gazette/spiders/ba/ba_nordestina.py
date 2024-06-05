from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaNordestinaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2922656"
    name = "ba_nordestina"
    allowed_domains = ["nordestina.ba.gov.br"]
    base_url = "https://www.nordestina.ba.gov.br"
    start_date = date(2009, 1, 21)
