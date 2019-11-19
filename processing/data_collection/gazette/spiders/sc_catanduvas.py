from gazette.spiders.base import FecamGazetteSpider


class ScCatanduvasSpider(FecamGazetteSpider):
    name = "sc_catanduvas"
    FECAM_QUERY = 'cod_entidade:66'
    TERRITORY_ID = "4204004"