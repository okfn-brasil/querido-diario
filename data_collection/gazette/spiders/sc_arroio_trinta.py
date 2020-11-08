from gazette.spiders.base import FecamGazetteSpider


class ScArroioTrintaSpider(FecamGazetteSpider):
    name = "sc_arroio_trinta"
    FECAM_QUERY = "cod_entidade:24"
    TERRITORY_ID = "4201604"
