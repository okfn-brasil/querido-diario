from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSaoJoseDaVitoriaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2929354"
    name = "ba_sao_jose_da_vitoria"
    allowed_domains = ["saojosedavitoria.ba.gov.br"]
    base_url = "https://www.saojosedavitoria.ba.gov.br"
    start_date = date(2008, 5, 5)
