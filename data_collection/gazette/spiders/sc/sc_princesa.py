from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPrincesaSpider(FecamGazetteSpider):
    name = "sc_princesa"
    FECAM_QUERY = "cod_entidade:213"
    TERRITORY_ID = "4214151"
