from gazette.spiders.base.fecam import FecamGazetteSpider


class ScForquilhinhaSpider(FecamGazetteSpider):
    name = "sc_forquilhinha"
    FECAM_QUERY = "cod_entidade:94"
    TERRITORY_ID = "4205456"
