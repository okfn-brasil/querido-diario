from gazette.spiders.base.fecam import FecamGazetteSpider


class ScGaropabaSpider(FecamGazetteSpider):
    name = "sc_garopaba"
    FECAM_QUERY = "cod_entidade:98"
    TERRITORY_ID = "4205704"
