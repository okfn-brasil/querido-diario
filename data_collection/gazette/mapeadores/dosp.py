from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorDosp(Mapeador):
    name = "dosp"
    format_url = "https://www.imprensaoficialmunicipal.com.br/@city"
    sep = "_"
    preference_state_code = "SP"
