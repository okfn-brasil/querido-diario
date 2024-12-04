from gazette.spiders.base.sigpub import BaseSigpubSpider


class MsAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "ms_associacao_municipios"
    TERRITORY_ID = "5000000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/ms"
