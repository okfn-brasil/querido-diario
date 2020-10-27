from gazette.spiders.base import FecamGazetteSpider


class ScPaialSpider(FecamGazetteSpider):
    name = "sc_paial"
    FECAM_QUERY = "cod_entidade:183"
    TERRITORY_ID = "4211876"
