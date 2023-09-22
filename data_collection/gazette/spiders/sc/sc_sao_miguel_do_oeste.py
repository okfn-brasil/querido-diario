from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaoMiguelDoOesteSpider(FecamGazetteSpider):
    name = "sc_sao_miguel_do_oeste"
    FECAM_QUERY = "cod_entidade:258"
    TERRITORY_ID = "4217204"
