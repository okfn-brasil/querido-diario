from gazette.spiders.base import FecamGazetteSpider


class ScConcordiaSpider(FecamGazetteSpider):
    name = "sc_concordia"
    FECAM_QUERY = "cod_entidade:73"
    TERRITORY_ID = "4204301"
