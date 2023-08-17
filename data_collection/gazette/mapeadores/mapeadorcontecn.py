from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorContecn(Mapeador):
    name = "mapeadorcontecn"

    def pattern_name(self):
        return "CONTECN"

    def valid_urls(self):
        return "vCONTECN"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://sandolandia.to.gov.br/diario-eletronico/
        # https://babaculandia.to.gov.br/diario-municipal
        # https://diariosantamariatocantins.com.br/  #TODO: esse layout de url não está na lista

        lista = [
            f"{protocol}://www.{city}.{state_code}.gov.br/diario-eletronico",
            f"{protocol}://{city}.{state_code}.gov.br/diario-municipal",
        ]
        return lista

    def validation(self, response):
        if "4sconexaoetecnologia.com.br" in response.text:
            if "Municipio ainda não possui" not in response.text:
                return True
        return False
