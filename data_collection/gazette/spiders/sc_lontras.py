from gazette.spiders.base.fecam import FecamGazetteSpider


class ScLontrasSpider(FecamGazetteSpider):
    name = "sc_lontras"
    FECAM_QUERY = "cod_entidade:153"
    TERRITORY_ID = "4209904"
