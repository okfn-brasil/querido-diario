from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorFECAM(Mapeador):
    name = "mapeadorfecam"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 100,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "FECAM"

    def valid_urls(self):
        return "vFECAM"

    def current_status(self):
        return "FECAM_status"

    def urls_pattern(self, protocol, city, state_code):
        pass

    def validation(self, response):
        pass

    def is_current(self, response):
        pass
