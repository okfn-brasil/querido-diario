from gazette.spiders.base.fecam import FecamGazetteSpider


class ScGasparSpider(FecamGazetteSpider):
    name = "sc_gaspar"
    FECAM_QUERY = "cod_entidade:100"
    TERRITORY_ID = "4205902"
