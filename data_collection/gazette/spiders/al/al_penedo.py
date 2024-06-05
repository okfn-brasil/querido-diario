from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class AlPenedoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2706703"
    name = "al_penedo"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/al/penedo"
    start_date = date(2013, 3, 27)
