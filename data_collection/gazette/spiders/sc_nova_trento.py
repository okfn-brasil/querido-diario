from gazette.spiders.base import FecamGazetteSpider


class ScNovaTrentoSpider(FecamGazetteSpider):
    name = "sc_nova_trento"
    FECAM_QUERY = "cod_entidade:176"
    TERRITORY_ID = "4211504"
