from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCaibiSpider(FecamGazetteSpider):
    name = "sc_caibi"
    FECAM_QUERY = "cod_entidade:54"
    TERRITORY_ID = "4203105"
