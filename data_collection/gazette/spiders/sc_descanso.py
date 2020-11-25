from gazette.spiders.base.fecam import FecamGazetteSpider


class ScDescansoSpider(FecamGazetteSpider):
    name = "sc_descanso"
    FECAM_QUERY = "cod_entidade:83"
    TERRITORY_ID = "4204905"
