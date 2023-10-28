from gazette.spiders.base.sigpub import SigpubGazetteSpider


class RjAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "rj_associacao_municipios"
    TERRITORY_ID = "3300000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/aemerj"
