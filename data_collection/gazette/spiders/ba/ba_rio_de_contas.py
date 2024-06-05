from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaRioDeContasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2926707"
    name = "ba_rio_de_contas"
    allowed_domains = ["riodecontas.ba.gov.br"]
    base_url = "https://www.riodecontas.ba.gov.br"
    start_date = date(2005, 9, 2)
