from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCapinzalSpider(FecamGazetteSpider):
    name = "sc_capinzal"
    FECAM_QUERY = "cod_entidade:64"
    TERRITORY_ID = "4203907"
