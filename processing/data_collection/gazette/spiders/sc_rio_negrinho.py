from gazette.spiders.base import FecamGazetteSpider


class ScRioNegrinhoSpider(FecamGazetteSpider):
    name = "sc_rio_negrinho"
    FECAM_QUERY = 'cod_entidade:222'
    TERRITORY_ID = "4215000"