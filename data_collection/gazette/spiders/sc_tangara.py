from gazette.spiders.base.fecam import FecamGazetteSpider


class ScTangaraSpider(FecamGazetteSpider):
    name = "sc_tangara"
    FECAM_QUERY = "cod_entidade:268"
    TERRITORY_ID = "4217907"
