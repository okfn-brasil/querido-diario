from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMaracajaSpider(FecamGazetteSpider):
    name = "sc_maracaja"
    FECAM_QUERY = "cod_entidade:160"
    TERRITORY_ID = "4210407"
