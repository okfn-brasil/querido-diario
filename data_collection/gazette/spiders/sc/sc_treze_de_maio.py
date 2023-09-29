from gazette.spiders.base.fecam import FecamGazetteSpider


class ScTrezeDeMaioSpider(FecamGazetteSpider):
    name = "sc_treze_de_maio"
    FECAM_QUERY = "cod_entidade:276"
    TERRITORY_ID = "4218400"
