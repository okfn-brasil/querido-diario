from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPapanduvaSpider(FecamGazetteSpider):
    name = "sc_papanduva"
    FECAM_QUERY = "cod_entidade:189"
    TERRITORY_ID = "4212205"
