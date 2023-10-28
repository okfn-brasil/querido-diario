from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MsBelaVistaSpider(BaseInstarSpider):
    TERRITORY_ID = "5002100"
    name = "ms_bela_vista"
    allowed_domains = ["belavista.ms.gov.br"]
    base_url = "https://www.belavista.ms.gov.br/portal/diario-oficial"
    start_date = date(2011, 11, 16)
