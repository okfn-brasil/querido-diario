from gazette.spiders.base.sai import SaiGazetteSpider


class BaMaragogipeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2920601"
    name = "ba_maragogipe"
    base_url = "https://sai.io.org.br/ba/maragojipe"
