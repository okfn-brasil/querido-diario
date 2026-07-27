from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class DiarioTipo:
    descricao: str

    @classmethod
    def from_dict(cls, data):
        return cls(descricao=data["descricao"])


@dataclass
class DiarioMidia:
    url: str

    @classmethod
    def from_dict(cls, data):
        return cls(url=data["url"])


@dataclass
class Diario:
    data: date
    numero: str
    tipo: DiarioTipo
    midias: list[DiarioMidia]

    @classmethod
    def from_dict(cls, data):
        return cls(
            data=parse_date(data["data"]),
            numero=data.get("numero", ""),
            tipo=DiarioTipo.from_dict(data["tipo"]),
            midias=[DiarioMidia.from_dict(m) for m in data.get("midias", [])],
        )

    @property
    def is_extra_edition(self):
        return is_extra_edition(self.tipo.descricao)

    @property
    def file_urls(self):
        return [m.url for m in self.midias if m.url]


@dataclass
class DiarioPage:
    current_page: int
    last_page: int
    diarios: list[Diario]

    @classmethod
    def from_response(cls, response):
        payload = response.json()
        return cls(
            current_page=payload["current_page"],
            last_page=payload["last_page"],
            diarios=[Diario.from_dict(d) for d in payload["data"]],
        )

    @property
    def has_next_page(self):
        return self.current_page < self.last_page

    @property
    def next_page(self):
        return self.current_page + 1


def parse_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d").date()


def is_extra_edition(tipo_descricao):
    tipo = tipo_descricao.lower()
    return "oficial" not in tipo and "semanal" not in tipo
