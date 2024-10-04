from gazette.spiders.base.sigpub import BaseSigpubSpider


class RnAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "rn_associacao_municipios"
    TERRITORY_ID = "2400000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/femurn"
