from gazette.spiders.base.fecam import FecamGazetteSpider


class ScAguasMornasSpider(FecamGazetteSpider):
    name = "sc_aguas_mornas"
    FECAM_QUERY = "cod_entidade:11"
    TERRITORY_ID = "4200606"
