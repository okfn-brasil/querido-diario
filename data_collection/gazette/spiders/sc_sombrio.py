from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSombrioSpider(FecamGazetteSpider):
    name = "sc_sombrio"
    FECAM_QUERY = "cod_entidade:265"
    TERRITORY_ID = "4217709"
