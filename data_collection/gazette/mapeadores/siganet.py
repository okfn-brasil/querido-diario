from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorSiganet(Mapeador):
    name = "siganet"
    format_url = "https://transparencia.@city.@uf.gov.br/diario"
    sep = ""
    preference_state_code = "MA"
