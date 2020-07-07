from gazette.spiders.base import FecamGazetteSpider


class ScPresidenteNereuSpider(FecamGazetteSpider):
    name = "sc_presidente_nereu"
    FECAM_QUERY = "cod_entidade:212"
    TERRITORY_ID = "4214102"
