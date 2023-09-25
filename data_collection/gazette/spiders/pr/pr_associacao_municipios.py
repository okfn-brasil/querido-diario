from gazette.spiders.base.sigpub import SigpubGazetteSpider


class PrAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "pr_associacao_municipios"
    TERRITORY_ID = "4100000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/amp"
