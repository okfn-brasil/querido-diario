from gazette.spiders.base.fecam import FecamGazetteSpider


class ScAuroraSpider(FecamGazetteSpider):
    name = "sc_aurora"
    FECAM_QUERY = "cod_entidade:28"
    TERRITORY_ID = "4201901"
