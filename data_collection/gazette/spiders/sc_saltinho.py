from gazette.spiders.base.fecam import FecamGazetteSpider


class ScSaltinhoSpider(FecamGazetteSpider):
    name = "sc_saltinho"
    FECAM_QUERY = "cod_entidade:228"
    TERRITORY_ID = "4215356"
