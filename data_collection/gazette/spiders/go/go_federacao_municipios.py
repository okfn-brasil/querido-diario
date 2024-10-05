from gazette.spiders.base.sigpub import BaseSigpubSpider


class GoFederacaoMunicipiosSpider(BaseSigpubSpider):
    name = "go_federacao_municipios"
    TERRITORY_ID = "5200001"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/fgm"
