from gazette.spiders.base.fecam import FecamGazetteSpider


class ScUrubiciSpider(FecamGazetteSpider):
    name = "sc_urubici"
    FECAM_QUERY = "cod_entidade:283"
    TERRITORY_ID = "4218905"
