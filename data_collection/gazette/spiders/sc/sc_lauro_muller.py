from gazette.spiders.base.fecam import FecamGazetteSpider


class ScLauroMullerSpider(FecamGazetteSpider):
    name = "sc_lauro_muller"
    FECAM_QUERY = "cod_entidade:149"
    TERRITORY_ID = "4209607"
