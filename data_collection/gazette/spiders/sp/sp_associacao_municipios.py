from gazette.spiders.base.sigpub import BaseSigpubSpider


class SpAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "sp_associacao_municipios"
    TERRITORY_ID = "3500000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/apm"
