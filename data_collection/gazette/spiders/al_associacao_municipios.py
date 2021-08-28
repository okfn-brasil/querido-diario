from gazette.spiders.base.sigpub import SigpubGazetteSpider


class AlAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "al_associacao_municipios"
    TERRITORY_ID = "2700001"
    CALENDAR_URL = "http://www.diariomunicipal.com.br/ama"
