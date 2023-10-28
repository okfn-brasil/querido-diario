from gazette.spiders.base.sigpub import SigpubGazetteSpider


class AlAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "al_associacao_municipios"
    TERRITORY_ID = "2700000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/ama"
