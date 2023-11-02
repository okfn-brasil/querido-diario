from gazette.spiders.base.fecam import FecamGazetteSpider


class ScLacerdopolisSpider(FecamGazetteSpider):
    name = "sc_lacerdopolis"
    FECAM_QUERY = "cod_entidade:144"
    TERRITORY_ID = "4209201"
