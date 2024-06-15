from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class AlIgaciSpider(SaiGazetteSpider):
    TERRITORY_ID = "2703106"
    name = "al_igaci"
    allowed_domains = ["igaci.al.gov.br"]
    base_url = "https://www.igaci.al.gov.br"
    start_date = date(2015, 7, 17)
