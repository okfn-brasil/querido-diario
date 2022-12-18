from datetime import date

from gazette.spiders.base.dionet import DionetGazetteSpider


class EsSerraSpider(DionetGazetteSpider):
    TERRITORY_ID = "3205002"
    name = "es_serra"
    allowed_domains = ["ioes.dio.es.gov.br"]

    start_date = date(2021, 1, 1)

    json_list_url = (
        "https://ioes.dio.es.gov.br"
        "/apifront/portal/edicoes/edicoes_from_data/{year}-{month}-{day}.json"
        "?subtheme=diariodaserra"
    )
    gazette_id_url = "https://ioes.dio.es.gov.br/portal/edicoes/download/{gazette_id}"
