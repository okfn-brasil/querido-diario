from gazette.spiders.base import FecamGazetteSpider


class ScLebonRegisSpider(FecamGazetteSpider):
    name = "sc_lebon_regis"
    FECAM_QUERY = "cod_entidade:150"
    TERRITORY_ID = "4209706"
