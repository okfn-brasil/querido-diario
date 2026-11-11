import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class CeAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "ce_associacao_municipios"
    TERRITORY_ID = "2300000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/aprece/"
    start_date = datetime.date(2010, 7, 1)

    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
    }
