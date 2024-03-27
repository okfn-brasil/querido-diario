from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorAplus(MapeadorSemantico):
    name = "mapeadoraplus"

    custom_settings = {
        "CONCURRENT_REQUESTS": 100,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "APLUS"

    def valid_urls(self):
        return "vAPLUS"

    def current_status(self):
        return "APLUS_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.bacabal.ma.gov.br/diario
        # https://www.codo.ma.gov.br/diario

        return [f"{protocol}://www.{city}.{state_code}.gov.br/diario/"]

    def validation(self, response):
        if "agenciaplus.com.br" in response.text:
            return True
        return False

    def is_current(self, response):
        rawdate = response.xpath(
            '//*[@id="content"]/div/div/div/a[1]/strong/text()'
        ).get()

        if "2024" in rawdate:
            return "atual"
        else:
            return "descontinuado"
