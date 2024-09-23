from gazette.spiders.base.sigpub import BaseSigpubSpider


class SeAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "se_associacao_municipios"
    TERRITORY_ID = "2800000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/sergipe"
