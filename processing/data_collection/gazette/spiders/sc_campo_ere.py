from gazette.spiders.base import FecamGazetteSpider


class ScCampoEreSpider(FecamGazetteSpider):
    name = "sc_campo_ere"
    FECAM_QUERY = "cod_entidade:59"
    TERRITORY_ID = "4203501"
