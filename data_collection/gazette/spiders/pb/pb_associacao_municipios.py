from gazette.spiders.base.sigpub import BaseSigpubSpider


class PbAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "pb_associacao_municipios"
    TERRITORY_ID = "2500000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/famup"
