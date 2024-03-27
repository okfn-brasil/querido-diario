from datetime import date

from gazette.spiders.base.dionet import DionetGazetteSpider


class EsAssociacaoMunicipiosSpider(DionetGazetteSpider):
    TERRITORY_ID = "3200000"
    name = "es_associacao_municipios"
    allowed_domains = ["ioes.dio.es.gov.br"]
    start_date = date(2021, 3, 1)

    BASE_URL = "https://ioes.dio.es.gov.br"
    url_subtheme = "?subtheme=dom"
