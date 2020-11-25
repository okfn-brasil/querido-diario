from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCapaoAltoSpider(FecamGazetteSpider):
    name = "sc_capao_alto"
    FECAM_QUERY = "cod_entidade:63"
    TERRITORY_ID = "4203253"
