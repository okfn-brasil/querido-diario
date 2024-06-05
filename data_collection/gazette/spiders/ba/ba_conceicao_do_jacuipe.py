from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaConceicaoDoJacuipeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2908507"
    name = "ba_conceicao_do_jacuipe"
    allowed_domains = ["conceicaodojacuipe.ba.gov.br"]
    base_url = "https://www.conceicaodojacuipe.ba.gov.br"
    start_date = date(2013, 1, 30)
