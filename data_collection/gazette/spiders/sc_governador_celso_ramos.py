from gazette.spiders.base.fecam import FecamGazetteSpider


class ScGovernadorCelsoRamosSpider(FecamGazetteSpider):
    name = "sc_governador_celso_ramos"
    FECAM_QUERY = "cod_entidade:101"
    TERRITORY_ID = "4206009"
