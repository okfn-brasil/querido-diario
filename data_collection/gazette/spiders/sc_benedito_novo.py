from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBeneditoNovoSpider(FecamGazetteSpider):
    name = "sc_benedito_novo"
    FECAM_QUERY = "cod_entidade:39"
    TERRITORY_ID = "4202206"
