import datetime

from gazette.spiders.base.sigpub import BaseSigpubSpider


class AlAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "al_associacao_municipios"
    PUBLIC_ENTITY_ID = "70001"
    GAZETTES_PAGE_URL = "https://www.diariomunicipal.com.br/ama/"
    start_date = datetime.date(2014, 4, 10)

    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
    }
