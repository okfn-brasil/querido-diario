from gazette.spiders.base.fecam import FecamGazetteSpider


class ScTunapolisSpider(FecamGazetteSpider):
    name = "sc_tunapolis"
    FECAM_QUERY = "cod_entidade:280"
    TERRITORY_ID = "4218756"
