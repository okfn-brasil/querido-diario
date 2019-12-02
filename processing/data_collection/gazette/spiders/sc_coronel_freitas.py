from gazette.spiders.base import FecamGazetteSpider


class ScCoronelFreitasSpider(FecamGazetteSpider):
    name = "sc_coronel_freitas"
    FECAM_QUERY = "cod_entidade:75"
    TERRITORY_ID = "4204400"
