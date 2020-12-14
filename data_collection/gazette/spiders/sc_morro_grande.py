from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMorroGrandeSpider(FecamGazetteSpider):
    name = "sc_morro_grande"
    FECAM_QUERY = "cod_entidade:172"
    TERRITORY_ID = "4211256"
