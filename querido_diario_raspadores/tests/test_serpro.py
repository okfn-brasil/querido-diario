import datetime as dt
import json
from unittest.mock import MagicMock

try:
    import pytest
except ImportError:
    pytest = None

from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse, TextResponse

from gazette.items import Gazette
from gazette.spiders.base.serpro import BaseSerproSpider
from gazette.spiders.rs.rs_bage import RsBageSpider


class SerproSpiderForTest(BaseSerproSpider):
    TERRITORY_ID = "0000000"
    name = "serpro_test"
    HASH_PREFEITURA = "test_hash_prefeitura_123"
    start_date = dt.date(2025, 1, 1)


def make_json_response(payload, url="https://cidadesdoe.serpro.gov.br/api", meta=None):
    return TextResponse(
        url=url,
        body=json.dumps(payload).encode("utf-8"),
        encoding="utf-8",
        request=MagicMock(meta=meta or {}),
    )


def make_text_response(body_text, url="https://cidadesdoe.serpro.gov.br/api", meta=None):
    return TextResponse(
        url=url,
        body=body_text.encode("utf-8") if isinstance(body_text, str) else body_text,
        encoding="utf-8",
        request=MagicMock(meta=meta or {}),
    )


def test_serpro_spider_requires_hash_prefeitura():
    """Valida que instanciar BaseSerproSpider sem HASH_PREFEITURA levanta NotConfigured."""
    class IncompleteSpider(BaseSerproSpider):
        TERRITORY_ID = "0000000"
        name = "incompleta"
        start_date = dt.date(2025, 1, 1)

    if pytest is not None:
        with pytest.raises(NotConfigured):
            IncompleteSpider()
    else:
        try:
            IncompleteSpider()
            assert False, "Deveria ter levantado NotConfigured"
        except NotConfigured:
            pass


def test_start_urls_constructed_from_hash():
    """Valida que a URL inicial é construída dinamicamente com o HASH_PREFEITURA."""
    spider = SerproSpiderForTest()
    assert len(spider.start_urls) == 1
    assert "Hash=test_hash_prefeitura_123" in spider.start_urls[0]
    assert spider.start_urls[0].startswith(spider.BASE_URL)


def test_parse_extracts_csrf_cookie_and_requests_module_info():
    """Valida que parse extrai o cookie de CSRF e requisita o manifesto de versão."""
    spider = SerproSpiderForTest()
    response = HtmlResponse(
        url=spider.start_urls[0],
        headers={"Set-Cookie": "crf=EXTRACTED_CSRF_TOKEN_789; path=/"},
        body=b"<html><body>Consulta Cidadao</body></html>",
        encoding="utf-8",
    )

    requests = list(spider.parse(response))
    assert len(requests) == 1
    req = requests[0]
    assert req.url.endswith("/moduleservices/moduleinfo")
    assert req.meta["csrf_token"] == "EXTRACTED_CSRF_TOKEN_789"
    assert req.callback == spider.parse_module_info


def test_parse_module_info_extracts_version_and_requests_first_page():
    """Valida a extração de versionToken e a emissão do request de busca paginada."""
    spider = SerproSpiderForTest(end="2025-01-31")
    manifest_payload = {"manifest": {"versionToken": "DYNAMIC_MODULE_VERSION_XYZ"}}
    response = make_json_response(
        manifest_payload,
        url=f"{spider.BASE_URL}/moduleservices/moduleinfo",
    )
    response.meta["csrf_token"] = "TOKEN_ABC"

    requests = list(spider.parse_module_info(response))
    assert len(requests) == 1
    req = requests[0]
    assert "DataActionBuscaPublicacaoComFiltro" in req.url
    assert req.method == "POST"
    assert req.headers["X-CSRFToken"] in ("TOKEN_ABC", b"TOKEN_ABC")

    payload = json.loads(req.body)
    assert payload["versionInfo"]["moduleVersion"] == "DYNAMIC_MODULE_VERSION_XYZ"
    assert payload["screenData"]["variables"]["StartIndex"] == 0
    assert payload["screenData"]["variables"]["Hash"] == "test_hash_prefeitura_123"


def test_pagination_does_not_truncate_count_above_25k():
    """Garante que contagens acima de 25.000 não são truncadas e a próxima página é requisitada."""
    spider = SerproSpiderForTest(end="2025-12-31")
    spider.logger = MagicMock()

    # Simula resposta com Count de 35.000 (acima do antigo limite de 25.000)
    items_list = [
        {
            "TB_DadosPublicacao": {
                "Id": f"{1000 + i}",
                "Dap_DataPublicacao": "2025-06-15T10:00:00Z",
                "Dap_Titulo": f"Publicação Diário Oficial nº {i + 1}",
                "Dap_ResumoPublicacao": "Atos Oficiais",
            }
        }
        for i in range(50)
    ]
    payload = {"data": {"Count": 35000, "List": items_list}}
    response = make_json_response(payload)
    response.meta.update({
        "start_index": 0,
        "module_version": "MOD_VER",
        "csrf_token": "CSRF_TOK",
    })

    requests = list(spider.parse_gazette_list(response))

    # Deve iniciar a cadeia de downloads com o primeiro item
    assert len(requests) == 1
    download_req = requests[0]
    assert "ActionBuscaArquivoPublicacao" in download_req.url
    assert download_req.meta["next_page_start_index"] == 50
    # O lote restante deve conter 49 publicações
    assert len(download_req.meta["remaining_items"]) == 49


def test_dispatch_next_download_configures_download_maxsize():
    """Garante que a requisição de download configura download_maxsize no meta do request."""
    spider = SerproSpiderForTest()
    items = [
        {
            "pub_id": "999",
            "date": dt.date(2025, 1, 10),
            "edition_number": "10",
            "is_extra_edition": False,
        }
    ]

    req = spider._dispatch_next_download_or_page(
        remaining_items=items,
        next_page_start_index=50,
        module_version="MOD_V",
        csrf_token="CSRF_V",
    )

    assert req is not None
    assert req.meta["download_maxsize"] == spider.MAX_RESPONSE_BODY_BYTES
    assert req.meta["download_warnsize"] == spider.MAX_RESPONSE_BODY_BYTES // 2
    assert req.meta["pub_id"] == "999"


def test_duplicate_page_fingerprint_stops_pagination():
    """Valida que uma página repetida identificada por MD5 interrompe a paginação."""
    spider = SerproSpiderForTest()
    spider.logger = MagicMock()

    payload = {
        "data": {
            "Count": 100,
            "List": [
                {
                    "TB_DadosPublicacao": {
                        "Id": "501",
                        "Dap_DataPublicacao": "2025-02-01T00:00:00Z",
                        "Dap_Titulo": "Edição 50",
                    }
                }
            ],
        }
    }
    response1 = make_json_response(payload)
    response1.meta.update({"start_index": 0})

    # Primeira requisição: processa normalmente
    reqs1 = list(spider.parse_gazette_list(response1))
    assert len(reqs1) == 1

    # Segunda requisição com exatamente os mesmos IDs: detecta duplicidade e encerra
    response2 = make_json_response(payload)
    response2.meta.update({"start_index": 50})
    reqs2 = list(spider.parse_gazette_list(response2))
    assert len(reqs2) == 0
    spider.logger.warning.assert_called()


def test_date_cutoff_stops_pagination_for_past_editions():
    """Valida que publicações anteriores a start_date encerram a paginação."""
    spider = SerproSpiderForTest()  # start_date = 2025-01-01
    spider.logger = MagicMock()

    payload = {
        "data": {
            "Count": 500,
            "List": [
                {
                    "TB_DadosPublicacao": {
                        "Id": "10",
                        "Dap_DataPublicacao": "2024-12-31T00:00:00Z",  # Anterior a 2025-01-01
                        "Dap_Titulo": "Edição Antiga",
                    }
                }
            ],
        }
    }
    response = make_json_response(payload)
    response.meta.update({"start_index": 0})

    requests = list(spider.parse_gazette_list(response))
    # Nenhuma requisição de download nem de próxima página deve ser emitida
    assert len(requests) == 0


def test_parse_gazette_file_emits_gazette_with_data_uri():
    """Valida a extração de Base64 e emissão de Gazette com Data URI RFC 2397."""
    spider = SerproSpiderForTest()
    b64_pdf = "JVBERi0xLjcKCjEgMCBvYmoKPDwvVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFI+PgplbmRvYmoK"
    payload = {"data": {"FileContent": b64_pdf}}

    response = make_json_response(payload)
    response.meta.update({
        "pub_id": "1234",
        "date": dt.date(2025, 1, 15),
        "edition_number": "42",
        "is_extra_edition": False,
        "power": "executive",
        "remaining_items": [],
        "next_page_start_index": None,
    })

    results = list(spider.parse_gazette_file(response))
    assert len(results) == 1

    item = results[0]
    assert isinstance(item, Gazette)
    assert item["date"] == dt.date(2025, 1, 15)
    assert item["edition_number"] == "42"
    assert item["is_extra_edition"] is False
    assert item["power"] == "executive"
    assert item["file_urls"] == [f"data:application/pdf;base64,{b64_pdf}"]


def test_parse_gazette_file_oversized_base64_logs_error_and_does_not_yield():
    """Garante que Base64 maior que MAX_PDF_B64_CHARS registra erro explícito e não emite item."""
    spider = SerproSpiderForTest()
    spider.logger = MagicMock()

    oversized_b64 = "A" * (spider.MAX_PDF_B64_CHARS + 1024)
    payload = {"data": {"FileContent": oversized_b64}}

    response = make_json_response(payload)
    response.meta.update({
        "pub_id": "9999",
        "date": dt.date(2025, 1, 15),
        "edition_number": "99",
        "is_extra_edition": False,
        "remaining_items": [],
        "next_page_start_index": None,
    })

    results = list(spider.parse_gazette_file(response))
    # Não deve emitir o Gazette
    assert len(results) == 0
    # Deve logar erro explícito com ID e data
    spider.logger.error.assert_called()
    error_message = spider.logger.error.call_args[0][0]
    assert "#9999" in error_message
    assert "Base64 de tamanho excessivo" in error_message


def test_parse_gazette_file_empty_base64_logs_error():
    """Garante que conteúdo Base64 vazio registra erro explícito e continua a esteira."""
    spider = SerproSpiderForTest()
    spider.logger = MagicMock()

    payload = {"data": {"FileContent": ""}}
    response = make_json_response(payload)
    response.meta.update({
        "pub_id": "8888",
        "date": dt.date(2025, 1, 15),
        "remaining_items": [],
        "next_page_start_index": None,
    })

    results = list(spider.parse_gazette_file(response))
    assert len(results) == 0
    spider.logger.error.assert_called()
    error_message = spider.logger.error.call_args[0][0]
    assert "#8888" in error_message


def test_handle_download_error_logs_and_dispatches_next():
    """Valida que erros de download/rede registram erro e continuam a esteira."""
    spider = SerproSpiderForTest()
    spider.logger = MagicMock()

    next_item = {
        "pub_id": "2222",
        "date": dt.date(2025, 1, 16),
        "edition_number": "43",
        "is_extra_edition": False,
    }

    mock_request = MagicMock()
    mock_request.meta = {
        "pub_id": "1111",
        "date": dt.date(2025, 1, 15),
        "remaining_items": [next_item],
        "next_page_start_index": None,
        "module_version": "V1",
        "csrf_token": "T1",
    }

    mock_failure = MagicMock()
    mock_failure.request = mock_request
    mock_failure.value = Exception("Connection closed before full body was received (download_maxsize exceeded)")

    requests = list(spider.handle_download_error(mock_failure))

    # Deve registrar erro com o ID da publicação que falhou
    spider.logger.error.assert_called()
    error_message = spider.logger.error.call_args[0][0]
    assert "#1111" in error_message

    # Deve continuar a esteira e emitir o download para a próxima publicação (2222)
    assert len(requests) == 1
    assert requests[0].meta["pub_id"] == "2222"


def test_parse_gazette_list_invalid_json_logs_error_and_stops():
    """Garante que resposta não-JSON na listagem loga erro e encerra graciosamente."""
    spider = SerproSpiderForTest()
    spider.logger = MagicMock()

    response = make_text_response(
        "<html><head><title>500 Internal Server Error</title></head></html>",
        meta={"start_index": 0},
    )

    requests = list(spider.parse_gazette_list(response))
    assert len(requests) == 0
    spider.logger.error.assert_called()
    assert "Falha ao decodificar JSON da listagem" in spider.logger.error.call_args[0][0]


def test_parse_gazette_file_invalid_json_logs_error_and_dispatches_next():
    """Garante que resposta não-JSON no download loga erro e despacha o próximo item."""
    spider = SerproSpiderForTest()
    spider.logger = MagicMock()

    next_item = {
        "pub_id": "3333",
        "date": dt.date(2025, 1, 16),
        "edition_number": "44",
        "is_extra_edition": False,
    }

    response = make_text_response(
        "bad json response",
        meta={
            "pub_id": "2222",
            "date": dt.date(2025, 1, 15),
            "remaining_items": [next_item],
            "next_page_start_index": None,
            "csrf_token": "CSRF_TOKEN_TEST",
            "module_version": "MOD_VER_TEST",
        },
    )

    requests = list(spider.parse_gazette_file(response))
    # Deve logar erro
    spider.logger.error.assert_called()
    # Deve continuar para o próximo item
    assert len(requests) == 1
    assert requests[0].meta["pub_id"] == "3333"


def test_parse_gazette_file_none_or_non_string_base64_logs_error_and_dispatches_next():
    """Garante que FileContent nulo ou não-string loga erro explícito e continua a esteira."""
    spider = SerproSpiderForTest()
    spider.logger = MagicMock()

    # Caso 1: FileContent é None
    payload_none = {"data": {"FileContent": None}}
    response_none = make_json_response(payload_none)
    response_none.meta.update({
        "pub_id": "4444",
        "date": dt.date(2025, 1, 15),
        "remaining_items": [],
        "next_page_start_index": None,
    })
    results_none = list(spider.parse_gazette_file(response_none))
    assert len(results_none) == 0
    spider.logger.error.assert_called()
    assert "#4444" in spider.logger.error.call_args[0][0]

    # Caso 2: FileContent não é string (ex: número ou objeto inesperado)
    spider.logger.reset_mock()
    payload_int = {"data": {"FileContent": 12345}}
    response_int = make_json_response(payload_int)
    response_int.meta.update({
        "pub_id": "5555",
        "date": dt.date(2025, 1, 15),
        "remaining_items": [],
        "next_page_start_index": None,
    })
    results_int = list(spider.parse_gazette_file(response_int))
    assert len(results_int) == 0
    spider.logger.error.assert_called()
    assert "#5555" in spider.logger.error.call_args[0][0]


def test_rs_bage_spider_configuration():
    """Valida que a spider concreta de Bagé - RS está devidamente configurada."""
    spider = RsBageSpider()
    assert issubclass(RsBageSpider, BaseSerproSpider)
    assert spider.TERRITORY_ID == "4301602"
    assert spider.name == "rs_bage"
    assert spider.start_date == dt.date(2024, 11, 8)
    assert spider.HASH_PREFEITURA == "eQJpm=Qsio5G=7tFAXJlF=hrIsVqGJ92JabaSQgbJFE="
    assert spider.power == "executive"

