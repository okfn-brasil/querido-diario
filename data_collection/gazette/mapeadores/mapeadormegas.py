from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorMegas(MapeadorSemantico):
    name = "mapeadormegas"

    def pattern_name(self):
        return "MEGAS"

    def valid_urls(self):
        return "vMEGAS"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://brejinhodenazare.to.gov.br/diariooficial/
        # https://arraias.to.gov.br/diariooficial/

        return [f"{protocol}://{city}.{state_code}.gov.br/diariooficial"]

    def validation(self, response):
        if "grupomegas.com" in response.text:
            return True
        return False
