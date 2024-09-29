from gazette.spiders.base.sigpub import BaseSigpubSpider


class MtAssociacaoMunicipiosSpider(BaseSigpubSpider):
    name = "mt_associacao_municipios"
    TERRITORY_ID = "5100000"
    CALENDAR_URL = "https://www.diariomunicipal.com.br/amm-mt"
