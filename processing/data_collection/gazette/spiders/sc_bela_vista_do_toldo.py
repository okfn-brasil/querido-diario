from gazette.spiders.base import FecamGazetteSpider


class ScBelaVistaDoToldoSpider(FecamGazetteSpider):
    name = "sc_bela_vista_do_toldo"
    FECAM_QUERY = "cod_entidade:37"
    TERRITORY_ID = "4202131"
