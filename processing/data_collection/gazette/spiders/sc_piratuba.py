from gazette.spiders.base import FecamGazetteSpider


class ScPiratubaSpider(FecamGazetteSpider):
    name = "sc_piratuba"
    FECAM_QUERY = 'cod_entidade:200'
    TERRITORY_ID = "4213104"