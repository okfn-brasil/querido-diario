from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorNucleogov(Mapeador):
    name = "mapeadornucleogov"

    def pattern_name(self):
        return "NUCGOV"

    def valid_urls(self):
        return "vNUCGOV"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://diariooficial.valparaisodegoias.go.gov.br/
        # https://dom.pirenopolis.go.gov.br/
        # https://diariooficial.jau.to.gov.br/

        lista = [
            f"{protocol}://diariooficial.{city}.{state_code}.gov.br/",
            f"{protocol}://dom.{city}.{state_code}.gov.br/",
        ]
        return lista

    def validation(self, response):
        if "nucleogov.com.br" in response.text:
            return True
        return False
