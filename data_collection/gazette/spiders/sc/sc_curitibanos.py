from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCuritibanosSpider(FecamGazetteSpider):
    name = "sc_curitibanos"
    FECAM_QUERY = "cod_entidade:82"
    TERRITORY_ID = "4204806"
