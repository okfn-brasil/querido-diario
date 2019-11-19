from gazette.spiders.base import FecamGazetteSpider


class ScPortoUniaoSpider(FecamGazetteSpider):
    name = "sc_porto_uniao"
    FECAM_QUERY = 'cod_entidade:207'
    TERRITORY_ID = "4213609"