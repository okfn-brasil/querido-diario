from gazette.spiders.base import FecamGazetteSpider


class ScSaoMiguelDaBoaVistaSpider(FecamGazetteSpider):
    name = "sc_sao_miguel_da_boa_vista"
    FECAM_QUERY = "cod_entidade:257"
    TERRITORY_ID = "4217154"
