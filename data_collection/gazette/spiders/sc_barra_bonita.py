from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBarraBonitaSpider(FecamGazetteSpider):
    name = "sc_barra_bonita"
    FECAM_QUERY = "cod_entidade:35"
    TERRITORY_ID = "4202099"
