from gazette.spiders.base import FecamGazetteSpider


class ScPlanaltoAlegreSpider(FecamGazetteSpider):
    name = "sc_planalto_alegre"
    FECAM_QUERY = 'cod_entidade:201'
    TERRITORY_ID = "4213153"