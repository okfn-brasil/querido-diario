from gazette.spiders.base.sigpub import SigpubGazetteSpider


class PeAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "pe_associacao_municipios"
    TERRITORY_ID = "2600000"
    CALENDAR_URL = "http://www.diariomunicipal.com.br/amupe"
