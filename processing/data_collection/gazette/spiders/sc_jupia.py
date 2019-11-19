from gazette.spiders.base import FecamGazetteSpider


class ScJupiaSpider(FecamGazetteSpider):
    name = "sc_jupia"
    FECAM_QUERY = 'cod_entidade:143'
    TERRITORY_ID = "4209177"