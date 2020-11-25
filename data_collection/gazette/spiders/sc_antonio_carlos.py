from gazette.spiders.base.fecam import FecamGazetteSpider


class ScAntonioCarlosSpider(FecamGazetteSpider):
    name = "sc_antonio_carlos"
    FECAM_QUERY = "cod_entidade:18"
    TERRITORY_ID = "4201208"
