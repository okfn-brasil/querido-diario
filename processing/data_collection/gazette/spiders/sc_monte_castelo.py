from gazette.spiders.base import FecamGazetteSpider


class ScMonteCasteloSpider(FecamGazetteSpider):
    name = "sc_monte_castelo"
    FECAM_QUERY = 'cod_entidade:170'
    TERRITORY_ID = "4211108"