from gazette.spiders.base.fecam import FecamGazetteSpider


class ScLuzernaSpider(FecamGazetteSpider):
    name = "sc_luzerna"
    FECAM_QUERY = "cod_entidade:155"
    TERRITORY_ID = "4210035"
