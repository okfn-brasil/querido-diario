from gazette.spiders.base.sigpub import SigpubGazetteSpider


class RoAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "ro_associacao_municipios"
    TERRITORY_ID = "1100000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/arom"
