from gazette.spiders.base.sigpub import BaseSigpubSpider


class SpMonteAltoSigpubSpider(BaseSigpubSpider):
    name = "sp_monte_alto_sigpub"
    TERRITORY_ID = "3531308"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/pmmasp"
