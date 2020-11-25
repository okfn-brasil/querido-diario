from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaoJoaquimSpider(FecamGazetteSpider):
    name = "sc_sao_joaquim"
    FECAM_QUERY = "cod_entidade:250"
    TERRITORY_ID = "4216503"
