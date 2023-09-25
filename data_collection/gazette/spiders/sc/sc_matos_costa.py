from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMatosCostaSpider(FecamGazetteSpider):
    name = "sc_matos_costa"
    FECAM_QUERY = "cod_entidade:164"
    TERRITORY_ID = "4210704"
