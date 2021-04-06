from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBracoDoTrombudoSpider(FecamGazetteSpider):
    name = "sc_braco_do_trombudo"
    FECAM_QUERY = "cod_entidade:50"
    TERRITORY_ID = "4202859"
