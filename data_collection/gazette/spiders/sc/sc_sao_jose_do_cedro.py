from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaoJoseDoCedroSpider(FecamGazetteSpider):
    name = "sc_sao_jose_do_cedro"
    FECAM_QUERY = "cod_entidade:252"
    TERRITORY_ID = "4216701"
