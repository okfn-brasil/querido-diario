from gazette.spiders.base import FecamGazetteSpider


class ScUrussangaSpider(FecamGazetteSpider):
    name = "sc_urussanga"
    FECAM_QUERY = "cod_entidade:285"
    TERRITORY_ID = "4219002"
