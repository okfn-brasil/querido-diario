from datetime import date

from gazette.spiders.base.dionet import DionetGazetteSpider


class EsAssociacaoMunicipiosSpider(DionetGazetteSpider):
    TERRITORY_ID = "3200000"
    name = "es_associacao_municipios"
    allowed_domains = ["ioes.dio.es.gov.br"]

    start_date = date(2021, 3, 1)

    json_list_url = (
        "https://ioes.dio.es.gov.br"
        "/apifront/portal/edicoes/edicoes_from_data/{year}-{month}-{day}.json"
        "?subtheme=dom"
    )
    gazette_id_url = "https://ioes.dio.es.gov.br/portal/edicoes/download/{gazette_id}"
