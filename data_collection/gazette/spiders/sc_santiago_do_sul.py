from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSantiagoDoSulSpider(FecamGazetteSpider):
    name = "sc_santiago_do_sul"
    FECAM_QUERY = "cod_entidade:237"
    TERRITORY_ID = "4215695"
