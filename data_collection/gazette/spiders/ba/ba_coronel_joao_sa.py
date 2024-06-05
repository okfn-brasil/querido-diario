from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCoronelJoaoSaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2909208"
    name = "ba_coronel_joao_sa"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/coroneljoaosa"
    start_date = date(2009, 3, 26)
