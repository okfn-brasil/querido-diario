from gazette.spiders.base.sigpub import BaseSigpubSpider


class PaFederacaoMunicipiosSpider(BaseSigpubSpider):
    name = "pa_federacao_municipios"
    TERRITORY_ID = "1500000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/famep"
