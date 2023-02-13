from gazette.spiders.base.sigpub import SigpubGazetteSpider


class SpAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "sp_associacao_municipios"
    TERRITORY_ID = "3500000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/apm"
