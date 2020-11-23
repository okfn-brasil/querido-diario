from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPetrolandiaSpider(FecamGazetteSpider):
    name = "sc_petrolandia"
    FECAM_QUERY = "cod_entidade:197"
    TERRITORY_ID = "4212700"
