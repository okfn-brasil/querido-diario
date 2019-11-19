from gazette.spiders.base import FecamGazetteSpider


class ScLajeadoGrandeSpider(FecamGazetteSpider):
    name = "sc_lajeado_grande"
    FECAM_QUERY = 'cod_entidade:147'
    TERRITORY_ID = "4209458"