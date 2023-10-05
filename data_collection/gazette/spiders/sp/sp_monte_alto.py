from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider
from gazette.spiders.base.sigpub import SigpubGazetteSpider


class SpMonteAltoSpider(BaseInstarSpider):
    TERRITORY_ID = "3531308"
    name = "sp_monte_alto"
    allowed_domains = ["montealto.instaridc.com.br"]
    start_date = date(2017, 9, 11)
    base_url = "http://montealto.instaridc.com.br/portal/diario-oficial"


class SpMonteAltoSigpubSpider(SigpubGazetteSpider):
    name = "sp_monte_alto_sigpub"
    TERRITORY_ID = "3531308"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/pmmasp"
