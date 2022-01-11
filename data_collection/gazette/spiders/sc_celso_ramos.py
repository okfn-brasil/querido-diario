from gazette.spiders.base.fecam import FecamGazetteSpider


class ScCelsoRamosSpider(FecamGazetteSpider):
    name = "sc_celso_ramos"
    FECAM_QUERY = "cod_entidade:68"
    TERRITORY_ID = "4204152"
