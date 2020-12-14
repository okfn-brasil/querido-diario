from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaoBentoDoSulSpider(FecamGazetteSpider):
    name = "sc_sao_bento_do_sul"
    FECAM_QUERY = "cod_entidade:239"
    TERRITORY_ID = "4215802"
