from gazette.spiders.base import FecamGazetteSpider


class ScPalmitosSpider(FecamGazetteSpider):
    name = "sc_palmitos"
    FECAM_QUERY = 'cod_entidade:188'
    TERRITORY_ID = "4212106"