from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorEPortal(Mapeador):
    name = "mapeadoreportal"

    custom_settings = {
        "CONCURRENT_REQUESTS": 100,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "EPORTAL"

    def valid_urls(self):
        return "vEPORTAL"

    def current_status(self):
        return "EPORTAL_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.riodosbois.to.gov.br/diariooficial
        # https://www.piraque.to.gov.br/diariooficial

        return [f"{protocol}://www.{city}.{state_code}.gov.br/diariooficial"]

    def validation(self, response):
        if "Termos de uso |" in response.text:
            if "Mantido por" in response.text:
                if "pratica-logo" in response.text:
                    return True
        return False

    def is_current(self, response):
        rawdate = response.xpath(
            "/html/body/section[1]/div/div/div[1]/div/div[1]/p[1]/text()"
        ).get()

        if "2024" in rawdate:
            return "atual"
        else:
            return "descontinuado"
