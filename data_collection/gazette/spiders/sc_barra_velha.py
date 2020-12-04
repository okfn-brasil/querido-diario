from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBarraVelhaSpider(FecamGazetteSpider):
    name = "sc_barra_velha"
    FECAM_QUERY = "cod_entidade:36"
    TERRITORY_ID = "4202107"
