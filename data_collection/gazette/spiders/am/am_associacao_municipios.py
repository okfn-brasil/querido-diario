from gazette.spiders.base.sigpub import BaseSigpubSpider


class AmAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "am_associacao_municipios"
    TERRITORY_ID = "1300000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/aam"
