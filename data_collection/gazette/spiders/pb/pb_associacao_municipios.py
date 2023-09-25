from gazette.spiders.base.sigpub import SigpubGazetteSpider


class PbAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "pb_associacao_municipios"
    TERRITORY_ID = "2500000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/famup"
