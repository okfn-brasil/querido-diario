from gazette.spiders.base.sigpub import BaseSigpubSpider


class BaAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "ba_associacao_municipios"
    TERRITORY_ID = "2900000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/amurc"
