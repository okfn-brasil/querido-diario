from gazette.spiders.base import FecamGazetteSpider


class ScBeneditoNovoSpider(FecamGazetteSpider):
    name = "sc_benedito_novo"
    FECAM_QUERY = 'cod_entidade:39'
    TERRITORY_ID = "4202206"