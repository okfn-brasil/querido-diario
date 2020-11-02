from gazette.spiders.base import FecamGazetteSpider


class ScEntreRiosSpider(FecamGazetteSpider):
    name = "sc_entre_rios"
    FECAM_QUERY = "cod_entidade:87"
    TERRITORY_ID = "4205175"
