from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaoJoaoBatistaSpider(FecamGazetteSpider):
    name = "sc_sao_joao_batista"
    FECAM_QUERY = "cod_entidade:246"
    TERRITORY_ID = "4216305"
