from gazette.spiders.base import FecamGazetteSpider


class ScMorroDaFumacaSpider(FecamGazetteSpider):
    name = "sc_morro_da_fumaca"
    FECAM_QUERY = "cod_entidade:171"
    TERRITORY_ID = "4211207"
