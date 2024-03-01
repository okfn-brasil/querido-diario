from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorMaxima(Mapeador):
    name = "mapeadormaxima"

    def pattern_name(self):
        return "MAX"

    def valid_urls(self):
        return "vMAX"

    def current_status(self):
        return "MAX_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://assuncao.pb.gov.br/publicacoes/boletim-oficial
        # https://boqueirao.pb.gov.br/publicacoes/jornal-oficial
        # https://caturite.pb.gov.br/publicacoes/diario-oficial
        # https://barradesantarosa.pb.gov.br/publicacoes/mensario-oficial
        # https://esperanca.pb.gov.br/publicacoes/quinzenarios

        lista = [
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/boletim-oficial",
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/jornal-oficial",
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/diario-oficial",
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/semanario-oficial",
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/mensario-oficial",
            f"{protocol}://{city}.{state_code}.gov.br/publicacoes/quinzenarios",
        ]
        return lista

    def validation(self, response):
        if "maxima.inf.br" in response.text:
            if "oficial" in response.url or "quinzenarios" in response.url:
                if "Nenhum resultado" not in response.text:
                    return True
        return False

    def is_current(self, response):
        raw = response.xpath('//*[@class="d-inline-block mb-0"]').get()

        if raw is None:
            return "vazio"
        elif "2024" in raw:
            return "atual"
        elif "20" in raw or "19" in raw:
            return "descontinuado"
        else:
            return "verificar"
