from gazette.spiders.base.fecam import FecamGazetteSpider


class ScIndaialSpider(FecamGazetteSpider):
    name = "sc_indaial"
    FECAM_QUERY = "cod_entidade:118"
    TERRITORY_ID = "4207502"
