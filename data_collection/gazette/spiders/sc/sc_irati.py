from gazette.spiders.base.fecam import FecamGazetteSpider


class ScIratiSpider(FecamGazetteSpider):
    name = "sc_irati"
    FECAM_QUERY = "cod_entidade:126"
    TERRITORY_ID = "4207858"
