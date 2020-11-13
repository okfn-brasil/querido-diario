from gazette.spiders.base.fecam import FecamGazetteSpider


class ScChapadaoDoLageadoSpider(FecamGazetteSpider):
    name = "sc_chapadao_do_lageado"
    FECAM_QUERY = "cod_entidade:70"
    TERRITORY_ID = "4204194"
