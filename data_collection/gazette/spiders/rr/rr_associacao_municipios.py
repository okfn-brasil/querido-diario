from gazette.spiders.base.sigpub import SigpubGazetteSpider


class RrAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "rr_associacao_municipios"
    TERRITORY_ID = "1400000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/amr"
