from gazette.spiders.base.sigpub import SigpubGazetteSpider


class BaAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "ba_associacao_municipios"
    TERRITORY_ID = "2900000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/amurc"
