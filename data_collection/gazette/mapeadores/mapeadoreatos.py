import json

from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorEatos(MapeadorSemantico):
    name = "mapeadoreatos"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 50,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "EATOS"

    def valid_urls(self):
        return "vEATOS"

    def current_status(self):
        return "EATOS_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://api.publicacoesmunicipais.com.br/api/v1/acts?page=1&pageSize=9&urlPath=brejogrande
        # https://api.publicacoesmunicipais.com.br/api/v1/acts?page=1&pageSize=9&urlPath=araua
        # https://api.publicacoesmunicipais.com.br/api/v1/acts?page=1&pageSize=9&urlPath=araras

        return [
            f"https://api.publicacoesmunicipais.com.br/api/v1/acts?page=1&pageSize=9&urlPath={city}"
        ]

    def validation(self, response):
        if "Falha na Operação" not in response.text:
            if "Falha ao listar Atos" not in response.text:
                if "Erro inesperado" not in response.text:
                    return True

    def is_current(self, response):
        recent = json.loads(response.text)["acts"][0]["date"]

        if "2024-" in recent:
            return "atual"
        elif "20" in recent or "19" in recent:
            return "descontinuado"
        else:
            return "verificar"
