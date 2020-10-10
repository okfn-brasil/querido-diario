from gazette.spiders.base import FecamGazetteSpider


class ScPousoRedondoSpider(FecamGazetteSpider):
    name = "sc_pouso_redondo"
    FECAM_QUERY = "cod_entidade:208"
    TERRITORY_ID = "4213708"
