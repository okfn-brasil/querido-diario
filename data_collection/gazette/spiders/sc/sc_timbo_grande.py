from gazette.spiders.base.fecam import FecamGazetteSpider


class ScTimboGrandeSpider(FecamGazetteSpider):
    name = "sc_timbo_grande"
    FECAM_QUERY = "cod_entidade:273"
    TERRITORY_ID = "4218251"
