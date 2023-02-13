from gazette.spiders.base.sigpub import SigpubGazetteSpider


class RsAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "rs_associacao_municipios"
    TERRITORY_ID = "4300000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/famurs"
