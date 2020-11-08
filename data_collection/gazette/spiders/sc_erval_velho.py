from gazette.spiders.base import FecamGazetteSpider


class ScErvalVelhoSpider(FecamGazetteSpider):
    name = "sc_erval_velho"
    FECAM_QUERY = "cod_entidade:89"
    TERRITORY_ID = "4205209"
