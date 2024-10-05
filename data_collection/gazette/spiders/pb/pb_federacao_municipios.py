from gazette.spiders.base.sigpub import BaseSigpubSpider


class PbFederacaoMunicipiosSpider(BaseSigpubSpider):
    name = "pb_federacao_municipios"
    TERRITORY_ID = "2500000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/famup"
