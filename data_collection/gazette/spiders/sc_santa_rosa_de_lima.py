from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSantaRosaDeLimaSpider(FecamGazetteSpider):
    name = "sc_santa_rosa_de_lima"
    FECAM_QUERY = "cod_entidade:233"
    TERRITORY_ID = "4215604"
