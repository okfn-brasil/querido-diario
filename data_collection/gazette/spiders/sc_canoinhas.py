from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCanoinhasSpider(FecamGazetteSpider):
    name = "sc_canoinhas"
    FECAM_QUERY = "cod_entidade:62"
    TERRITORY_ID = "4203808"
