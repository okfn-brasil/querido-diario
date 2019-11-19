from gazette.spiders.base import FecamGazetteSpider


class ScCamboriuSpider(FecamGazetteSpider):
    name = "sc_camboriu"
    FECAM_QUERY = 'cod_entidade:56'
    TERRITORY_ID = "4203204"