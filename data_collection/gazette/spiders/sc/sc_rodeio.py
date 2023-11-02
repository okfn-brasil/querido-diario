from gazette.spiders.base.fecam import FecamGazetteSpider


class ScRodeioSpider(FecamGazetteSpider):
    name = "sc_rodeio"
    FECAM_QUERY = "cod_entidade:225"
    TERRITORY_ID = "4215109"
