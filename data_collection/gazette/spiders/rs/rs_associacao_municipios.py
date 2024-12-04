from gazette.spiders.base.sigpub import BaseSigpubSpider


class RsAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "rs_associacao_municipios"
    TERRITORY_ID = "4300000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/famurs"
