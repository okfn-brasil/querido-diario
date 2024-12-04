from gazette.spiders.base.sigpub import BaseSigpubSpider


class PiAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "pi_associacao_municipios"
    TERRITORY_ID = "2200000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/appm"
