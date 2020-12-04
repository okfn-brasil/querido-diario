from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaoCarlosSpider(FecamGazetteSpider):
    name = "sc_sao_carlos"
    FECAM_QUERY = "cod_entidade:242"
    TERRITORY_ID = "4216008"
