from gazette.spiders.base.sigpub import BaseSigpubSpider


class GoAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "go_associacao_municipios_agm"
    TERRITORY_ID = "5200000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/agm"
