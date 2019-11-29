from gazette.spiders.base import FecamGazetteSpider


class ScSaoJoseSpider(FecamGazetteSpider):
    name = "sc_sao_jose"
    FECAM_QUERY = "cod_entidade:251"
    TERRITORY_ID = "4216602"
