from gazette.spiders.base.fecam import FecamGazetteSpider


class ScLindoiaDoSulSpider(FecamGazetteSpider):
    name = "sc_lindoia_do_sul"
    FECAM_QUERY = "cod_entidade:152"
    TERRITORY_ID = "4209854"
