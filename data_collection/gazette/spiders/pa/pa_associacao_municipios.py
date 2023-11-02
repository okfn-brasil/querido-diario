from gazette.spiders.base.sigpub import SigpubGazetteSpider


class PaAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "pa_associacao_municipios"
    TERRITORY_ID = "1500000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/famep"
