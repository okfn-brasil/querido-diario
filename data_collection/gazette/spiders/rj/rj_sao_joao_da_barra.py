from datetime import date

from gazette.spiders.base.portalgov import BasePortalGovSpider


class RjSaoJoaoDaBarraSpider(BasePortalGovSpider):
    name = "rj_sao_joao_da_barra"
    TERRITORY_ID = "3305000"
    allowed_domains = ["sjb.rj.gov.br"]
    start_date = date(2013, 7, 15)
    domain = "www.sjb.rj.gov.br"
