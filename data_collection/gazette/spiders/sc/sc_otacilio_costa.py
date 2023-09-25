from gazette.spiders.base.fecam import FecamGazetteSpider


class ScOtacilioCostaSpider(FecamGazetteSpider):
    name = "sc_otacilio_costa"
    FECAM_QUERY = "cod_entidade:180"
    TERRITORY_ID = "4211751"
