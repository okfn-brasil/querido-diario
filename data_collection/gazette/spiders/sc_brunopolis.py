from gazette.spiders.base.fecam import FecamGazetteSpider


class ScBrunopolisSpider(FecamGazetteSpider):
    name = "sc_brunopolis"
    FECAM_QUERY = "cod_entidade:51"
    TERRITORY_ID = "4202875"
