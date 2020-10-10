from gazette.spiders.base import FecamGazetteSpider


class ScIomereSpider(FecamGazetteSpider):
    name = "sc_iomere"
    FECAM_QUERY = "cod_entidade:119"
    TERRITORY_ID = "4207577"
