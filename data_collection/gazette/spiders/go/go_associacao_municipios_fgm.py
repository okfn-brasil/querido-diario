from gazette.spiders.base.sigpub import SigpubGazetteSpider


class GoAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "go_associacao_municipios_fgm"
    TERRITORY_ID = "5200000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/fgm"
