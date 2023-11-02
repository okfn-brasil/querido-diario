from gazette.spiders.base.sigpub import SigpubGazetteSpider


class MsAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "ms_associacao_municipios"
    TERRITORY_ID = "5000000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/ms"
