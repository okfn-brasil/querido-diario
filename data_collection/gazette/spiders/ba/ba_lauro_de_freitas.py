from gazette.spiders.base.sai import SaiGazetteSpider


class BaLauroDeFreitasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2920601"
    name = "ba_lauro_de_freitas"
    base_url = "https://sai.io.org.br/ba/laurodefreitas"
