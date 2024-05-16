from gazette.spiders.base.fecam import FecamGazetteSpider


class ScMirimDoceSpider(FecamGazetteSpider):
    name = "sc_mirim_doce"
    FECAM_QUERY = "cod_entidade:166"
    TERRITORY_ID = "4210852"
