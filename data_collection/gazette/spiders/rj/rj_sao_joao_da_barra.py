from datetime import date

from gazette.spiders.base.portalgov import BasePortalGovSpider


class RjSaoJoaoDaBarraSpider(BasePortalGovSpider):
    name = "rj_sao_joao_da_barra"
    TERRITORY_ID = "3305000"
    start_date = date(2013, 7, 15)
    website = "www.sjb.rj.gov.br"
    power = "executive"
