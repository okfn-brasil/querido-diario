from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorMaxima(Mapeador):
    name = "mapeadormaxima"

    def pattern_name(self):
        return "MAX"

    def valid_urls(self):
        return "vMAX"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://assuncao.pb.gov.br/publicacoes/boletim-oficial
        # https://boqueirao.pb.gov.br/publicacoes/jornal-oficial
        # https://caturite.pb.gov.br/publicacoes/diario-oficial
        # https://barradesantarosa.pb.gov.br/publicacoes/mensario-oficial

        lista = [
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/boletim-oficial",
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/jornal-oficial",
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/diario-oficial",
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/mensario-oficial",
        ]
        return lista

    def validation(self, response):
        if "maxima.inf.br" in response.text:
            if "Nenhum resultado" not in response.text:
                return True
        return False
