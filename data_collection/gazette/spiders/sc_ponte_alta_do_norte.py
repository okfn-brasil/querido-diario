from gazette.spiders.base.fecam import FecamGazetteSpider


class ScPonteAltaDoNorteSpider(FecamGazetteSpider):
    name = "sc_ponte_alta_do_norte"
    FECAM_QUERY = "cod_entidade:204"
    TERRITORY_ID = "4213351"
