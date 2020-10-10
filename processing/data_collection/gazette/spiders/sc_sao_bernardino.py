from gazette.spiders.base import FecamGazetteSpider


class ScSaoBernardinoSpider(FecamGazetteSpider):
    name = "sc_sao_bernardino"
    FECAM_QUERY = "cod_entidade:240"
    TERRITORY_ID = "4215752"
