from gazette.spiders.base.fecam import FecamGazetteSpider


class ScErmoSpider(FecamGazetteSpider):
    name = "sc_ermo"
    FECAM_QUERY = "cod_entidade:88"
    TERRITORY_ID = "4205191"
