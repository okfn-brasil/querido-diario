from gazette.spiders.base import FecamGazetteSpider


class ScPassoDeTorresSpider(FecamGazetteSpider):
    name = "sc_passo_de_torres"
    FECAM_QUERY = 'cod_entidade:191'
    TERRITORY_ID = "4212254"