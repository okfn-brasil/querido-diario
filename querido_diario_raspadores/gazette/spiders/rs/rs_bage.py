import datetime as dt
import hashlib
import json
import re
import urllib.parse
from typing import Any, Generator, Optional

import scrapy
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RsBageSpider(BaseGazetteSpider):
    """
    Raspador de diários oficiais da Prefeitura Municipal de Bagé - RS.

    Município: Bagé - RS
    Código IBGE: 4301602
    Plataforma de publicação: SERPRO Gov.br Cidades (DOE - Documento Oficial Eletrônico)
    Iniciativa e desenvolvimento: Bagé Transparente (www.bagetransparente.com.br)

    Arquitetura conservadora de coleta, compatível com o padrão de spiders do projeto
    e sem sobrescrever as configurações globais do Scrapy:
    - Cadeia sequencial de downloads: apenas um download de PDF ativo por vez;
    - Uso de memória limitado a um lote de no máximo PAGE_SIZE publicações;
    - A próxima página de listagem só é requisitada após a conclusão do lote atual;
    - 5 barreiras independentes contra loops infinitos de paginação;
    - Validação de teto de resposta HTTP antes do parsing JSON;
    - Teto de Base64 (25 MB) calibrado para o porte do DOE de Bagé;
    - Sem sobrescrever configurações globais do framework (sem custom_settings).
    """

    TERRITORY_ID = "4301602"
    name = "rs_bage"
    allowed_domains = ["cidadesdoe.serpro.gov.br"]

    # Data da edição inaugural do DOE eletrônico de Bagé no SERPRO
    start_date = dt.date(2024, 11, 8)

    BASE_URL = "https://cidadesdoe.serpro.gov.br/govbrcidades_doe"
    HASH_PREFEITURA = "eQJpm=Qsio5G=7tFAXJlF=hrIsVqGJ92JabaSQgbJFE="

    # Tokens e versões de fallback caso o manifesto oscile
    DEFAULT_CSRF_TOKEN = "T6C+9iB49TLra4jEsMeSckDMNhQ="
    DEFAULT_MODULE_VERSION = "n+Mjd8q_ahkeNIkyYfbTNA"
    DEFAULT_API_VERSION_SEARCH = "zRAHqBwfWZSZQDXDYGpfWg"
    DEFAULT_API_VERSION_DOWNLOAD = "p6Pwyi8dX2Lf8E0FKxeCTw"

    # -------------------------------------------------------------------------
    # LIMITES RÍGIDOS OPERACIONAIS (BARREIRAS DE SEGURANÇA E MEMÓRIA)
    # -------------------------------------------------------------------------
    PAGE_SIZE = 50
    MAX_PAGES_LIMIT = 500             # Barreira 1: Máximo de 500 páginas (25.000 publicações)
    MAX_START_INDEX = 25000           # Barreira 2: Teto absoluto do índice de paginação
    MAX_CONSECUTIVE_NO_PROGRESS = 2   # Barreira 5: Aborta se 2 páginas seguidas não trouxerem IDs válidos
    MAX_RESPONSE_BODY_BYTES = 30 * 1024 * 1024  # Teto de bytes brutos HTTP antes do parsing JSON (30 MB)
    MAX_PDF_B64_CHARS = 25 * 1024 * 1024        # Barreira de Base64: ~18 MB binário máximo (calibrado para Bagé)
    REQUEST_TIMEOUT = 35              # Timeout máximo por requisição individual (segundos)

    # URL inicial pública para abertura de sessão e cookies automáticos via Scrapy
    start_urls = [
        f"https://cidadesdoe.serpro.gov.br/govbrcidades_doe/DoeConsultaCidadao?&Hash=eQJpm=Qsio5G=7tFAXJlF=hrIsVqGJ92JabaSQgbJFE="
    ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # Estado operacional interno
        self.seen_pub_ids: set[str] = set()
        self.seen_page_fingerprints: set[str] = set()
        self.pages_crawled = 0
        self.consecutive_no_progress = 0

    def parse(self, response: scrapy.http.Response) -> Generator[scrapy.Request, None, None]:
        """
        Recebe a resposta da página inicial pública, captura cookies no CookieJar
        e requisita o manifesto dinâmico para validação de versão do OutSystems.
        """
        self._inc_stat("bage/initial_requests")
        csrf_token = self.DEFAULT_CSRF_TOKEN

        set_cookies = response.headers.getlist("Set-Cookie")
        for cookie_raw in set_cookies:
            try:
                cookie_str = urllib.parse.unquote(cookie_raw.decode("utf-8", errors="ignore"))
                match = re.search(r"crf=([^;]+)", cookie_str)
                if match:
                    csrf_token = match.group(1)
                    break
            except Exception:
                continue

        manifest_url = f"{self.BASE_URL}/moduleservices/moduleinfo"
        yield scrapy.Request(
            url=manifest_url,
            callback=self.parse_module_info,
            meta={
                "csrf_token": csrf_token,
                "download_timeout": self.REQUEST_TIMEOUT,
                "max_retry_times": 3,
            },
            errback=self.handle_request_error,
            dont_filter=True,
        )

    def parse_module_info(
        self, response: scrapy.http.Response
    ) -> Generator[scrapy.Request, None, None]:
        """
        Extrai dinamicamente o versionToken do OutSystems e inicia a primeira página.
        """
        csrf_token = response.meta.get("csrf_token", self.DEFAULT_CSRF_TOKEN)
        module_version = self.DEFAULT_MODULE_VERSION

        try:
            info = json.loads(response.text)
            if isinstance(info, dict):
                token = info.get("manifest", {}).get("versionToken")
                if token and isinstance(token, str):
                    module_version = token
                    self._inc_stat("bage/dynamic_version_detected")
        except (json.JSONDecodeError, AttributeError):
            self.logger.warning(
                "Falha ao decodificar moduleinfo do SERPRO. Utilizando versão padrão validada."
            )
            self._inc_stat("bage/moduleinfo_fallback")

        yield self._build_page_request(
            start_index=0,
            module_version=module_version,
            csrf_token=csrf_token,
        )

    def _build_page_request(
        self, start_index: int, module_version: str, csrf_token: str
    ) -> scrapy.Request:
        """Monta a requisição POST de listagem de metadados com cabeçalhos sanitizados."""
        endpoint = (
            f"{self.BASE_URL}/screenservices/govbrcidades_doe/Cidadao/"
            f"DOEConsultaCidadao/ScreenDataSetGetTBDadosPublicacaoByDapIdHashPrefeitura"
        )

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json",
            "X-CSRFToken": csrf_token,
            "Origin": "https://cidadesdoe.serpro.gov.br",
            "Referer": f"{self.BASE_URL}/DoeConsultaCidadao?&Hash={self.HASH_PREFEITURA}",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        }

        payload = {
            "versionInfo": {
                "moduleVersion": module_version,
                "apiVersion": self.DEFAULT_API_VERSION_SEARCH,
            },
            "viewName": "Cidadao.DOEConsultaCidadao",
            "screenData": {
                "variables": {
                    "Filtro": {
                        "IdHashPrefeitura": "",
                        "TermoTitulo": "",
                        "TermoResumo": "",
                        "OrgaoId": "0",
                        "DataInicio": self.start_date.isoformat(),
                        "DataFim": self.end_date.isoformat(),
                        "TipoDocumento": "0",
                    },
                    "ExibirDownloadConfirmacao": False,
                    "TableSort": "",
                    "StrPaginacao": {
                        "MaxRecord": self.PAGE_SIZE,
                        "StartIndex": start_index,
                        "IndexPagAtual": 1,
                        "NumPaginas": "1",
                        "TotalCount": 0,
                        "TextItens": "",
                        "ListRegPagPaginacao": {"List": []},
                        "SelNumRegPorPagina": self.PAGE_SIZE,
                        "SelPagPaginacao": 1,
                    },
                    "DownloadArquivo": {
                        "NomeArquivo": "",
                        "TamanhoArquivo": "",
                        "ConteudoArquivo": None,
                        "IdDadosPublicacao": "0",
                    },
                    "LimpaPesquisa": False,
                    "DataSiteKey": "",
                    "Secret": "",
                    "DadosPublicacao_Id": "0",
                    "EnableButtonPesquisar": False,
                    "ShowSpinner": False,
                    "ShowOrgao": True,
                    "Hash": self.HASH_PREFEITURA,
                    "_hashInDataFetchStatus": 1,
                }
            },
            "inputParameters": {
                "StartIndex": start_index,
                "MaxRecords": self.PAGE_SIZE,
            },
            "clientVariables": {
                "CpfLogado": "",
                "Perfil": "",
                "NomeUsuario": "",
                "IsLogado": False,
                "HashEntidade": self.HASH_PREFEITURA,
                "NomePrefeitura": "",
                "ResponseToken": "",
                "PrefeituraId": "7",
                "PerfilOriginal": "",
                "IsEntidadePublica": False,
            },
        }

        return scrapy.Request(
            url=endpoint,
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse_gazette_list,
            meta={
                "start_index": start_index,
                "module_version": module_version,
                "csrf_token": csrf_token,
                "download_timeout": self.REQUEST_TIMEOUT,
                "max_retry_times": 3,
            },
            errback=self.handle_request_error,
            dont_filter=True,
        )

    def parse_gazette_list(
        self, response: scrapy.http.Response
    ) -> Generator[scrapy.Request, None, None]:
        """
        Processa a resposta JSON da listagem com as 5 barreiras de segurança contra loops
        e inicia a cadeia sequencial unitária de downloads.
        """
        module_version = response.meta.get("module_version", self.DEFAULT_MODULE_VERSION)
        csrf_token = response.meta.get("csrf_token", self.DEFAULT_CSRF_TOKEN)
        start_index = response.meta.get("start_index", 0)

        # BARREIRA 1: Limite Máximo de Páginas
        self.pages_crawled += 1
        self._inc_stat("bage/pages_crawled")
        if self.pages_crawled > self.MAX_PAGES_LIMIT:
            self.logger.warning(
                f"[Barreira 1 Ativada] Limite máximo de {self.MAX_PAGES_LIMIT} páginas atingido. Encerrando."
            )
            self._inc_stat("bage/stop_max_pages_limit")
            return

        # BARREIRA 2: Teto Máximo de StartIndex
        if start_index >= self.MAX_START_INDEX:
            self.logger.warning(
                f"[Barreira 2 Ativada] StartIndex {start_index} excedeu o teto seguro de {self.MAX_START_INDEX}. Encerrando."
            )
            self._inc_stat("bage/stop_max_index_limit")
            return

        # Validação HTTP e decodificação JSON defensiva
        try:
            data = json.loads(response.text)
            if not isinstance(data, dict):
                raise ValueError("Payload de resposta não é um dicionário JSON.")
        except Exception as err:
            self.logger.error(f"Resposta inválida (não JSON) na página start_index={start_index}: {err}")
            self._inc_stat("bage/api_json_errors")
            return

        data_block = data.get("data", {})
        if not isinstance(data_block, dict):
            self.logger.error(f"Estrutura 'data' ausente ou inválida no start_index={start_index}.")
            self._inc_stat("bage/api_structure_errors")
            return

        total_count = self._sanitize_count(data_block.get("Count", 0))

        raw_list = data_block.get("List", {})
        if isinstance(raw_list, dict):
            items = raw_list.get("List", [])
        elif isinstance(raw_list, list):
            items = raw_list
        else:
            items = []

        if not items:
            self.logger.info(f"Página start_index={start_index} retornou sem itens. Fim da listagem.")
            self._inc_stat("bage/stop_empty_page")
            return

        # BARREIRA 3: Detecção de Página Repetida (Fingerprint não criptográfico)
        page_id_sequence = ",".join(
            str(it.get("TB_DadosPublicacao", {}).get("Id", ""))
            for it in items
            if isinstance(it, dict)
        )
        page_fingerprint = hashlib.md5(page_id_sequence.encode("utf-8"), usedforsecurity=False).hexdigest()
        if page_fingerprint in self.seen_page_fingerprints:
            self.logger.warning(
                f"[Barreira 3 Ativada] Página duplicada detectada (hash {page_fingerprint[:8]}). A API travou no mesmo lote. Encerrando."
            )
            self._inc_stat("bage/stop_repeated_page")
            return
        self.seen_page_fingerprints.add(page_fingerprint)

        # Filtra os itens válidos e prepara a esteira em memória
        valid_items_batch = []
        new_valid_ids_count = 0
        hit_date_cutoff = False

        for item in items:
            if not isinstance(item, dict):
                continue

            pub = item.get("TB_DadosPublicacao", {})
            if not isinstance(pub, dict):
                continue

            pub_id = pub.get("Id")
            raw_date = pub.get("Dap_DataPublicacao")
            title = str(pub.get("Dap_Titulo") or "").strip()
            summary = str(pub.get("Dap_ResumoPublicacao") or "").strip()

            if not pub_id or not raw_date:
                self._inc_stat("bage/gazettes_invalid_payload")
                continue

            str_pub_id = str(pub_id).strip()

            # BARREIRA 4: Deduplicação de publicações individuais
            if str_pub_id in self.seen_pub_ids:
                self._inc_stat("bage/gazettes_duplicate_skipped")
                continue

            # Parsing defensivo de data
            try:
                date_part = str(raw_date).split("T")[0]
                gazette_date = dt.datetime.strptime(date_part, "%Y-%m-%d").date()
            except (ValueError, IndexError, AttributeError):
                self.logger.warning(f"Data inválida na publicação #{str_pub_id}: {raw_date}")
                self._inc_stat("bage/gazettes_invalid_date")
                continue

            # Corte Temporal: Encerra se a publicação for anterior a start_date
            if gazette_date < self.start_date:
                self.logger.info(
                    f"Alcançada publicação #{str_pub_id} ({gazette_date}) anterior a start_date ({self.start_date})."
                )
                self._inc_stat("bage/stop_date_cutoff")
                hit_date_cutoff = True
                break

            if gazette_date > self.end_date:
                self._inc_stat("bage/gazettes_future_skipped")
                continue

            # Somente após validação completa de ID, data e período, registra como processado
            self.seen_pub_ids.add(str_pub_id)
            new_valid_ids_count += 1
            self._inc_stat("bage/gazettes_found")

            edition_number = self._extract_edition_number(title)
            is_extra = "extra" in title.lower() or "extra" in summary.lower()

            valid_items_batch.append({
                "pub_id": str_pub_id,
                "date": gazette_date,
                "edition_number": edition_number,
                "is_extra_edition": is_extra,
            })

        # BARREIRA 5: Detecção de Ausência de Progresso
        if new_valid_ids_count == 0:
            self.consecutive_no_progress += 1
            if self.consecutive_no_progress >= self.MAX_CONSECUTIVE_NO_PROGRESS:
                self.logger.warning(
                    f"[Barreira 5 Ativada] {self.consecutive_no_progress} páginas consecutivas sem novos IDs válidos. Encerrando."
                )
                self._inc_stat("bage/stop_no_progress")
                return
        else:
            self.consecutive_no_progress = 0

        # Se não há itens válidos para download nesta página:
        if not valid_items_batch:
            if not hit_date_cutoff and (start_index + self.PAGE_SIZE) < total_count:
                yield self._build_page_request(
                    start_index=start_index + self.PAGE_SIZE,
                    module_version=module_version,
                    csrf_token=csrf_token,
                )
            return

        # Inverte a lista para permitir remoção O(1) com pop() na ponta
        valid_items_batch.reverse()

        # INICIA A CADEIA SEQUENCIAL DE DOWNLOADS (EXATAMENTE 1 PDF ATIVO POR VEZ)
        next_page_start_index = (start_index + self.PAGE_SIZE) if (not hit_date_cutoff and (start_index + self.PAGE_SIZE) < total_count) else None

        req = self._dispatch_next_download_or_page(
            remaining_items=valid_items_batch,
            next_page_start_index=next_page_start_index,
            module_version=module_version,
            csrf_token=csrf_token,
        )
        if req:
            yield req

    def _dispatch_next_download_or_page(
        self,
        remaining_items: list[dict[str, Any]],
        next_page_start_index: Optional[int],
        module_version: str,
        csrf_token: str,
    ) -> Optional[scrapy.Request]:
        """
        Dispara o próximo download unitário ou, se o lote terminou, requisita a próxima página.
        Garante apenas um download de PDF ativo por vez, com memória limitada pelo lote atual.
        """
        if remaining_items:
            # Remoção O(1) do final da lista invertida
            current_item = remaining_items.pop()
            download_url = (
                f"{self.BASE_URL}/screenservices/govbrcidades_doe/"
                f"ActionBuscaArquivoPublicacao"
            )
            download_payload = {
                "versionInfo": {
                    "moduleVersion": module_version,
                    "apiVersion": self.DEFAULT_API_VERSION_DOWNLOAD,
                },
                "viewName": "Cidadao.DOEConsultaCidadao",
                "inputParameters": {
                    "TB_DadosPublicacaoIdentifier_Input": str(current_item["pub_id"]),
                    "HashPrefeitura_Input": self.HASH_PREFEITURA,
                },
            }

            gazette_meta = {
                "date": current_item["date"],
                "edition_number": current_item["edition_number"],
                "is_extra_edition": current_item["is_extra_edition"],
                "power": "executive",
                "pub_id": current_item["pub_id"],
                "remaining_items": remaining_items,
                "next_page_start_index": next_page_start_index,
                "module_version": module_version,
                "csrf_token": csrf_token,
                "download_timeout": self.REQUEST_TIMEOUT,
                "max_retry_times": 3,
            }

            return scrapy.Request(
                url=download_url,
                method="POST",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Accept": "application/json",
                    "X-CSRFToken": csrf_token,
                    "Origin": "https://cidadesdoe.serpro.gov.br",
                    "Referer": f"{self.BASE_URL}/DoeConsultaCidadao?&Hash={self.HASH_PREFEITURA}",
                },
                body=json.dumps(download_payload),
                callback=self.parse_gazette_file,
                meta=gazette_meta,
                errback=self.handle_download_error,
                dont_filter=True,
            )

        # Se não há mais itens restantes no lote, avança para a próxima página
        if next_page_start_index is not None:
            return self._build_page_request(
                start_index=next_page_start_index,
                module_version=module_version,
                csrf_token=csrf_token,
            )

        return None

    def parse_gazette_file(
        self, response: scrapy.http.Response
    ) -> Generator[Any, None, None]:
        """
        Processa o download do arquivo atual, emite o Gazette e imediatamente despacha o próximo download,
        garantindo apenas um download de PDF ativo por vez e memória limitada pelo lote atual.
        """
        meta = response.meta
        pub_id = meta.get("pub_id", "desconhecido")
        remaining_items = meta.get("remaining_items", [])
        next_page_start_index = meta.get("next_page_start_index")
        module_version = meta.get("module_version", self.DEFAULT_MODULE_VERSION)
        csrf_token = meta.get("csrf_token", self.DEFAULT_CSRF_TOKEN)

        # BARREIRA PRÉVIA: Validação de tamanho do corpo HTTP antes de qualquer parsing JSON
        raw_body = getattr(response, "body", b"") or b""
        if len(raw_body) > self.MAX_RESPONSE_BODY_BYTES:
            self.logger.error(
                f"[Teto HTTP Ativado] Resposta da publicação #{pub_id} ({len(raw_body)} bytes) excede o limite seguro de {self.MAX_RESPONSE_BODY_BYTES} bytes. Descartada antes do parsing JSON."
            )
            self._inc_stat("bage/download_rejected_too_large")
            next_req = self._dispatch_next_download_or_page(
                remaining_items=remaining_items,
                next_page_start_index=next_page_start_index,
                module_version=module_version,
                csrf_token=csrf_token,
            )
            if next_req:
                yield next_req
            return

        try:
            data = json.loads(response.text)
            if not isinstance(data, dict):
                raise ValueError("Resposta de download não é um objeto JSON válido.")
            data_block = data.get("data", {})
            b64_content = data_block.get("FileContent") or data_block.get("Arquivo_Output")
        except Exception as err:
            self.logger.error(f"Erro ao decodificar JSON do arquivo da publicação #{pub_id}: {err}")
            self._inc_stat("bage/download_json_errors")
            b64_content = None

        if not b64_content or not isinstance(b64_content, str):
            self.logger.warning(
                f"Publicação #{pub_id} de {meta.get('date')} não retornou conteúdo Base64 válido."
            )
            self._inc_stat("bage/download_empty_base64")
        elif len(b64_content) > self.MAX_PDF_B64_CHARS:
            # Proteção contra PDF Gigante (após JSON)
            self.logger.error(
                f"[Teto de RAM Ativado] Publicação #{pub_id} ({len(b64_content)} chars > {self.MAX_PDF_B64_CHARS}) descartada para proteger a memória."
            )
            self._inc_stat("bage/download_rejected_too_large")
        else:
            # Emite o Gazette para o pipeline com Data URI
            pdf_data_uri = f"data:application/pdf;base64,{b64_content}"
            self._inc_stat("bage/gazettes_downloaded")

            yield Gazette(
                date=meta["date"],
                edition_number=meta["edition_number"],
                is_extra_edition=meta["is_extra_edition"],
                power=meta["power"],
                file_urls=[pdf_data_uri],
            )

        # CONTINUAÇÃO DA CADEIA: dispara o próximo download unitário ou a próxima página
        next_req = self._dispatch_next_download_or_page(
            remaining_items=remaining_items,
            next_page_start_index=next_page_start_index,
            module_version=module_version,
            csrf_token=csrf_token,
        )
        if next_req:
            yield next_req

    def handle_download_error(self, failure: Any) -> Generator[scrapy.Request, None, None]:
        """
        Tratamento defensivo: se um download falhar por timeout ou rede,
        não interrompe a esteira e continua para o próximo arquivo.
        """
        self.logger.error(f"Falha de transporte ao baixar PDF: {repr(failure.value)}")
        self._inc_stat("bage/download_network_failures")

        request = getattr(failure, "request", None)
        if request and hasattr(request, "meta"):
            meta = request.meta
            next_req = self._dispatch_next_download_or_page(
                remaining_items=meta.get("remaining_items", []),
                next_page_start_index=meta.get("next_page_start_index"),
                module_version=meta.get("module_version", self.DEFAULT_MODULE_VERSION),
                csrf_token=meta.get("csrf_token", self.DEFAULT_CSRF_TOKEN),
            )
            if next_req:
                yield next_req

    def handle_request_error(self, failure: Any) -> None:
        """Tratamento de falhas de rede na listagem."""
        self.logger.error(f"Falha de rede na listagem: {repr(failure.value)}")
        self._inc_stat("bage/network_failures")

    def _extract_edition_number(self, title: str) -> Optional[str]:
        """Extração segura do número de edição com proteção contra ReDoS."""
        if not title:
            return None
        truncated = title[:150]
        match = re.search(r"n[º°\.\s]*(\d+)", truncated, re.IGNORECASE)
        return match.group(1) if match else None

    def _sanitize_count(self, raw_count: Any) -> int:
        """Sanitização estrita do total de registros retornado pela API."""
        try:
            count = int(raw_count)
            if count < 0:
                return 0
            return min(count, self.MAX_START_INDEX)
        except (ValueError, TypeError):
            return 0

    def _inc_stat(self, key: str, count: int = 1) -> None:
        """Incrementa contador estatístico do Scrapy se o crawler estiver ativo."""
        if hasattr(self, "crawler") and self.crawler and hasattr(self.crawler, "stats") and self.crawler.stats:
            self.crawler.stats.inc_value(key, count)
