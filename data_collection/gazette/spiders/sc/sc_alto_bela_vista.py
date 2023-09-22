from gazette.spiders.base.fecam import FecamGazetteSpider


class ScAltoBelaVistaSpider(FecamGazetteSpider):
    name = "sc_alto_bela_vista"
    FECAM_QUERY = "cod_entidade:13"
    TERRITORY_ID = "4200754"
