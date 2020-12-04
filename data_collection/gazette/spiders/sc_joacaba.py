from gazette.spiders.base.fecam import FecamGazetteSpider


class ScJoacabaSpider(FecamGazetteSpider):
    name = "sc_joacaba"
    FECAM_QUERY = "cod_entidade:140"
    TERRITORY_ID = "4209003"
