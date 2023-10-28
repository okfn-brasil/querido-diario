from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPeritibaSpider(FecamGazetteSpider):
    name = "sc_peritiba"
    FECAM_QUERY = "cod_entidade:196"
    TERRITORY_ID = "4212601"
