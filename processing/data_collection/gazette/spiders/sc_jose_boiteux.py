from gazette.spiders.base import FecamGazetteSpider


class ScJoseBoiteuxSpider(FecamGazetteSpider):
    name = "sc_jose_boiteux"
    FECAM_QUERY = "cod_entidade:142"
    TERRITORY_ID = "4209151"
