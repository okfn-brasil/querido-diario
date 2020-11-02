from gazette.spiders.base import FecamGazetteSpider


class ScPresidenteCastelloBrancoSpider(FecamGazetteSpider):
    name = "sc_presidente_castello_branco"
    FECAM_QUERY = "cod_entidade:210"
    TERRITORY_ID = "4213906"
