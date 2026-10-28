from datetime import date

from scrapy.http import HtmlResponse

from gazette.spiders.base.dioenet import BaseDioenetSpider

BASE_URL = "https://plenussistemas.dioenet.com.br/list/municipio-teste"


class DioenetSpiderForTest(BaseDioenetSpider):
    TERRITORY_ID = "0000000"
    name = "dioenet_test"
    start_date = date(2023, 10, 1)
    BASE_URL = BASE_URL
    power = "executive"


def gazette_li(number, day, ementa=""):
    return f"""
    <li>
      <div class="col-one">
        <h3>Diário Oficial de {day} <span class="badge badge-b">Edição nº {number}</span></h3>
      </div>
      <div class="col-two">
        <div class="btn-group">
          <a href="https://plenussistemas.dioenet.com.br/uploads/view/{number}"
             title="Diário de {day} - Edição nº {number} "
             class="btn btn-default btn-sm">Visualizar Edição nº {number}</a>
        </div>
      </div>
      <div class="ementa-section"><h4>Ementa</h4>{ementa}</div>
    </li>
    """


def make_response(body):
    return HtmlResponse(
        url=f"{BASE_URL}?d=05%2F10%2F2023+a+12%2F10%2F2023&pagina=1",
        body=f'<ul class="lista-diarios">{body}</ul>'.encode("utf-8"),
        encoding="utf-8",
    )


def test_parse_ignores_lists_nested_in_the_ementa():
    # Santana do Garambéu/MG publica ementas com <ul><li>. Esses <li> internos
    # não são edições e não podem interromper a leitura da página.
    ementa = "<ul><li>Abertura de propostas dia 25/10/2023</li><li>Modo de Disputa: Aberto</li></ul>"
    response = make_response(
        gazette_li(57, "10/10/2023", ementa) + gazette_li(56, "06/10/2023")
    )
    spider = DioenetSpiderForTest()

    requests = list(
        spider.parse(response, params={"d": "05/10/2023 a 12/10/2023", "pagina": "1"})
    )

    items = [r.cb_kwargs["gazette_item"] for r in requests]
    assert [item["edition_number"] for item in items] == ["57", "56"]
    assert items[1]["date"] == date(2023, 10, 6)
    assert all(item["is_extra_edition"] is False for item in items)
