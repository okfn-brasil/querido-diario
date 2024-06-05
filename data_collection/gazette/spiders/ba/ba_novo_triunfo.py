from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaNovoTriunfoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2923050"
    name = "ba_novo_triunfo"
    allowed_domains = ["novotriunfo.ba.gov.br"]
    base_url = "https://www.novotriunfo.ba.gov.br"
    start_date = date(2015, 1, 14)
