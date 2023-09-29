from gazette.spiders.base.fecam import FecamGazetteSpider


class ScIraniSpider(FecamGazetteSpider):
    name = "sc_irani"
    FECAM_QUERY = "cod_entidade:125"
    TERRITORY_ID = "4207809"
