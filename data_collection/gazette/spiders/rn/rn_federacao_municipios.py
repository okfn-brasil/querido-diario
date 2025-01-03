from gazette.spiders.base.sigpub import BaseSigpubSpider


class RnFederacaoMunicipiosSpider(BaseSigpubSpider):
    name = "rn_federacao_municipios"
    TERRITORY_ID = "2400000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/femurn"
