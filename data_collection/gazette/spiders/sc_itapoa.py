from gazette.spiders.base import FecamGazetteSpider


class ScItapoaSpider(FecamGazetteSpider):
    name = "sc_itapoa"
    FECAM_QUERY = "cod_entidade:133"
    TERRITORY_ID = "4208450"
