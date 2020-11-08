from gazette.spiders.base import FecamGazetteSpider


class ScSaoDomingosSpider(FecamGazetteSpider):
    name = "sc_sao_domingos"
    FECAM_QUERY = "cod_entidade:244"
    TERRITORY_ID = "4216107"
