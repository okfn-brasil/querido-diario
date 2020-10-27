from gazette.spiders.base import FecamGazetteSpider


class ScSaudadesSpider(FecamGazetteSpider):
    name = "sc_saudades"
    FECAM_QUERY = "cod_entidade:260"
    TERRITORY_ID = "4217303"
