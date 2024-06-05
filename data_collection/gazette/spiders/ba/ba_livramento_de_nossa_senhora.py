from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaLivramentoDeNossaSenhoraSpider(SaiGazetteSpider):
    TERRITORY_ID = "2919504"
    name = "ba_livramento_de_nossa_senhora"
    allowed_domains = ["livramentodenossasenhora.ba.gov.br"]
    base_url = "https://www.livramentodenossasenhora.ba.gov.br"
    start_date = date(2007, 4, 23)
