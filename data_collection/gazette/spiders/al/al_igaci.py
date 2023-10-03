from gazette.spiders.base.sai import SaiGazetteSpider


class AlIgaciSpider(SaiGazetteSpider):
    TERRITORY_ID = "2703106"
    name = "al_igaci"
    base_url = "https://www.igaci.al.gov.br"
