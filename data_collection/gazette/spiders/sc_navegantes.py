from gazette.spiders.base.fecam import FecamGazetteSpider


class ScNavegantesSpider(FecamGazetteSpider):
    name = "sc_navegantes"
    FECAM_QUERY = "cod_entidade:173"
    TERRITORY_ID = "4211306"
