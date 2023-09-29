from gazette.spiders.base.fecam import FecamGazetteSpider


class ScItajaiSpider(FecamGazetteSpider):
    name = "sc_itajai"
    FECAM_QUERY = 'entidade:"Prefeitura municipal de Itajaí"'
    TERRITORY_ID = "4208203"
