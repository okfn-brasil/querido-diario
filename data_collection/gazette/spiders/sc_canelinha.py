from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCanelinhaSpider(FecamGazetteSpider):
    name = "sc_canelinha"
    FECAM_QUERY = "cod_entidade:61"
    TERRITORY_ID = "4203709"
