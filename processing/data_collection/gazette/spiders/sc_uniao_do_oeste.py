from gazette.spiders.base import FecamGazetteSpider


class ScUniaoDoOesteSpider(FecamGazetteSpider):
    name = "sc_uniao_do_oeste"
    FECAM_QUERY = 'cod_entidade:282'
    TERRITORY_ID = "4218855"