from gazette.spiders.base.sigpub import BaseSigpubSpider


class RoAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "ro_associacao_municipios"
    TERRITORY_ID = "1100000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/arom"
