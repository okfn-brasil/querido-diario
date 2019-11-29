from gazette.spiders.base import FecamGazetteSpider


class ScVidalRamosSpider(FecamGazetteSpider):
    name = "sc_vidal_ramos"
    FECAM_QUERY = "cod_entidade:289"
    TERRITORY_ID = "4219200"
