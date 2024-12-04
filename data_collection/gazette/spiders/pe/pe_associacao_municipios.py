from gazette.spiders.base.sigpub import BaseSigpubSpider


class PeAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "pe_associacao_municipios"
    TERRITORY_ID = "2600000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/amupe"
