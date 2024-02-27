from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorCR2(Mapeador):
    name = "mapeadorcr2"

    custom_settings = {
        "CONCURRENT_REQUESTS": 50,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "CR2"

    def valid_urls(self):
        return "vCR2"

    def current_status(self):
        return "CR2_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://vigia.pa.gov.br/c/publicacoes/diario-oficial/
        # https://altamira.pa.gov.br/c/publicacoes/diario-oficial/

        return [
            f"{protocol}://{city}.{state_code}.gov.br/c/publicacoes/diario-oficial/",
            f"{protocol}://{city}.{state_code}.gov.br/c/publicacoes/",
            f"{protocol}://pm{city}.{state_code}.gov.br/c/publicacoes/",
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes-oficiais/"
            f"{protocol}://{city}.{state_code}.gov.br/",
        ]

    def validation(self, response):
        if "Desenvolvido por CR2" in response.text or "logo-cr2" in response.text:
            return True
        return False

    def is_current(self, response):
        raw = response.xpath('//*[@class="month"]').get()
        if raw is None:
            current = "verificar"
        elif "/2024" in raw:
            current = "atual"
        elif "/20" in raw or "/19" in raw:
            current = "descontinuado"
        elif "Nada encontrado" in raw:
            current = "vazio"

        if "diario-oficial" in response.url:
            return "completo-" + current
        elif "publicacoes" not in response.url:
            return "validado (ver)"
        else:
            return "fragmentado-" + current
