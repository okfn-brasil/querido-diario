from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMajorVieiraSpider(FecamGazetteSpider):
    name = "sc_major_vieira"
    FECAM_QUERY = "cod_entidade:159"
    TERRITORY_ID = "4210308"
