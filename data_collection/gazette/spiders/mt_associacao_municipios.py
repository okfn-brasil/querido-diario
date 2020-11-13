from gazette.spiders.base.sigpub import SigpubGazetteSpider


class MtAssociacaoMunicipiosSpider(SigpubGazetteSpider):
    name = "mt_associacao_municipios"
    TERRITORY_ID = "5100000"
    CALENDAR_URL = "http://www.diariomunicipal.com.br/amm-mt"
