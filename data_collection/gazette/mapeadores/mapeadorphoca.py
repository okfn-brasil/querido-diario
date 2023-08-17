from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorPhoca(Mapeador):
    name = "mapeadorphoca"

    def pattern_name(self):
        return "PHOCA"

    def valid_urls(self):
        return "vPHOCA"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.abreulandia.to.gov.br/diariooficial
        # http://www.fatima.to.gov.br/diariooficial
        # http://www.doisirmaos.to.gov.br/diariooficial #TODO: outro formato de url, nome abreviado

        return [
            f"{protocol}://www.{city}.{state_code}.gov.br/diariooficial",
            f"{protocol}://diariooficial.{city}.{state_code}.gov.br/todas-edicoes",
        ]

    def validation(self, response):
        if "phoca.cz" in response.text:
            return True
        return False
