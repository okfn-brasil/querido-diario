from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMaravilhaSpider(FecamGazetteSpider):
    name = "sc_maravilha"
    FECAM_QUERY = "cod_entidade:161"
    TERRITORY_ID = "4210506"
