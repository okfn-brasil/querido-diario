import datetime as dt
import hashlib
import json
import re
import urllib.parse
from typing import Any, Generator, Optional

import scrapy
from scrapy.exceptions import NotConfigured

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseSerproSpider(BaseGazetteSpider):
    """
    Spider base para portais de Diário Oficial Eletrônico (DOE)
    geridos pela plataforma SERPRO Gov.br Cidades (OutSystems).

    Para adicionar um novo município que utiliza esta plataforma,
    basta herdar desta classe e definir:
    - `TERRITORY_ID`: Código IBGE do município (ex: "4301602")
    - `name`: Nome da spider no formato <uf>_<município> (ex: "rs_bage")
    - `start_date`: Data da primeira edição disponível (ex: dt.date(2024, 11, 8))
    - `HASH_PREFEITURA`: Hash de identificação da prefeitura no SERPRO
    - `power`: Poder publicador (padrão: "executive")
    """

    allowed_domains = ["cidadesdoe.serpro.gov.br"]
    BASE_URL = "https://cidadesdoe.serpro.gov.br/govbrcidades_doe"
    power = "executive"

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
    MAX_PDF_B64_CHARS = 25 * 1024 * 1024        # Barreira de Base64: ~18,75 MB binário máximo
    REQUEST_TIMEOUT = 35              # Timeout máximo por requisição individual (segundos)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not hasattr(self, "HASH_PREFEITURA"):
            raise NotConfigured("Please set a value for `HASH_PREFEITURA`")

        # Define a URL inicial dinâmica com base no hash da prefeitura
        self.start_urls = [
            f"{self.BASE_URL}/DoeConsultaCidadao?&Hash={self.HASH_PREFEITURA}"
        ]

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
        self._inc_stat("serpro/initial_requests")
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
        Valida o manifesto de versão retornado pela plataforma OutSystems e
        despacha a primeira requisição de busca paginada.
        """
        csrf_token = response.meta.get("csrf_token", self.DEFAULT_CSRF_TOKEN)
        module_version = self.DEFAULT_MODULE_VERSION

        try:
            manifest_data = json.loads(response.text)
            if isinstance(manifest_data, dict):
                if "manifest" in manifest_data and isinstance(manifest_data["manifest"], dict):
                    module_version = manifest_data["manifest"].get("versionToken", module_version)
                    self.logger.info(f"Versão de módulo SERPRO obtida dinamicamente: {module_version}")
                elif "versionToken" in manifest_data:
                    module_version = manifest_data.get("versionToken", module_version)
                    self.logger.info(f"Versão de módulo SERPRO obtida dinamicamente: {module_version}")
        except Exception as err:
            self.logger.warning(
                f"Não foi possível parsear manifesto de versão ({err}). Usando fallback padrão: {module_version}"
            )

        yield self._build_page_request(
            start_index=0,
            module_version=module_version,
            csrf_token=csrf_token,
        )

    def _build_page_request(
        self,
        start_index: int,
        module_version: str,
        csrf_token: str,
    ) -> scrapy.Request:
        """
        Constrói a requisição POST para o endpoint REST da listagem paginada.
        """
        search_url = (
            f"{self.BASE_URL}/screenservices/GovBRCidades_DOE/DoeConsultaCidadao/"
            f"DOEConsultaCidadao/DataActionBuscaPublicacaoComFiltro"
            f"?{self.DEFAULT_API_VERSION_SEARCH}"
        )
        search_payload = {
            "versionInfo": {
                "moduleVersion": module_version,
                "apiVersion": self.DEFAULT_API_VERSION_SEARCH,
            },
            "viewName": "DoeConsultaCidadao.DOEConsultaCidadao",
            "screenData": {
                "variables": {
                    "Hash": self.HASH_PREFEITURA,
                    "Inp_DataInicio": self.start_date.strftime("%Y-%m-%d"),
                    "Inp_DataFim": self.end_date.strftime("%Y-%m-%d"),
                    "Inp_Titulo": "",
                    "Inp_NumeroEdicao": "",
                    "Inp_SecretariaId": 0,
                    "Inp_TipoPublicacaoId": 0,
                    "StartIndex": start_index,
                    "MaxRecords": self.PAGE_SIZE,
                }
            },
        }

        return scrapy.Request(
            url=search_url,
            method="POST",
            headers={
                "Content-Type": "application/json; charset=UTF-8",
                "Accept": "application/json",
                "X-CSRFToken": csrf_token,
                "Origin": "https://cidadesdoe.serpro.gov.br",
                "Referer": f"{self.BASE_URL}/DoeConsultaCidadao?&Hash={self.HASH_PREFEITURA}",
            },
            body=json.dumps(search_payload),
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
        Interpreta a lista JSON retornada pelo SERPRO, aplica as 5 barreiras de proteção
        contra loops infinitos e inicia a cadeia sequencial de downloads unitários.
        """
        meta = response.meta
        start_index = meta.get("start_index", 0)
        module_version = meta.get("module_version", self.DEFAULT_MODULE_VERSION)
        csrf_token = meta.get("csrf_token", self.DEFAULT_CSRF_TOKEN)

        self.pages_crawled += 1
        self._inc_stat("serpro/pages_crawled")

        # BARREIRA 1: Limite máximo estrito de páginas
        if self.pages_crawled > self.MAX_PAGES_LIMIT:
            self.logger.warning(
                f"[Barreira 1 Ativada] Atingido o teto de {self.MAX_PAGES_LIMIT} páginas. Encerrando paginação."
            )
            self._inc_stat("serpro/stop_max_pages_reached")
            return

        # BARREIRA 2: Teto máximo de StartIndex
        if start_index > self.MAX_START_INDEX:
            self.logger.warning(
                f"[Barreira 2 Ativada] StartIndex {start_index} excedeu o teto seguro de {self.MAX_START_INDEX}. Encerrando."
            )
            self._inc_stat("serpro/stop_max_start_index_reached")
            return

        # Parsing de resposta JSON
        try:
            data = json.loads(response.text)
            if not isinstance(data, dict):
                raise ValueError("Resposta da listagem não é um dicionário JSON válido.")
            data_block = data.get("data", {})
            raw_items = data_block.get("List", [])
            if isinstance(raw_items, dict):
                raw_items = raw_items.get("List", [])
            total_count = self._sanitize_count(data_block.get("Count", 0))
        except Exception as err:
            self.logger.error(f"Falha ao decodificar JSON da listagem na página {self.pages_crawled}: {err}")
            self._inc_stat("serpro/list_json_errors")
            return

        # BARREIRA 3: Fingerprint criptográfico da página
        sorted_item_ids = sorted(
            [
                str(item.get("TB_DadosPublicacao", {}).get("Id"))
                for item in raw_items
                if isinstance(item, dict) and item.get("TB_DadosPublicacao", {}).get("Id")
            ]
        )
        page_fingerprint = hashlib.md5(
            ":".join(sorted_item_ids).encode("utf-8"), usedforsecurity=False
        ).hexdigest()
        if page_fingerprint in self.seen_page_fingerprints and len(sorted_item_ids) > 0:
            self.logger.warning(
                f"[Barreira 3 Ativada] Página duplicada identificada por fingerprint MD5 ({page_fingerprint}). Encerrando paginação."
            )
            self._inc_stat("serpro/stop_duplicate_page_fingerprint")
            return
        if len(sorted_item_ids) > 0:
            self.seen_page_fingerprints.add(page_fingerprint)

        self.logger.info(
            f"Processando página {self.pages_crawled} (StartIndex: {start_index}, Itens brutos: {len(raw_items)}, Total estimado: {total_count})"
        )

        valid_items_batch = []
        new_valid_ids_count = 0
        hit_date_cutoff = False

        for item in raw_items:
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
                self._inc_stat("serpro/gazettes_invalid_payload")
                continue

            str_pub_id = str(pub_id).strip()

            # BARREIRA 4: Deduplicação de publicações individuais
            if str_pub_id in self.seen_pub_ids:
                self._inc_stat("serpro/gazettes_duplicate_skipped")
                continue

            # Parsing defensivo de data
            try:
                date_part = str(raw_date).split("T")[0]
                gazette_date = dt.datetime.strptime(date_part, "%Y-%m-%d").date()
            except (ValueError, IndexError, AttributeError):
                self.logger.warning(f"Data inválida na publicação #{str_pub_id}: {raw_date}")
                self._inc_stat("serpro/gazettes_invalid_date")
                continue

            # Corte Temporal: Encerra se a publicação for anterior a start_date
            if gazette_date < self.start_date:
                self.logger.info(
                    f"Alcançada publicação #{str_pub_id} ({gazette_date}) anterior a start_date ({self.start_date})."
                )
                self._inc_stat("serpro/stop_date_cutoff")
                hit_date_cutoff = True
                break

            if gazette_date > self.end_date:
                self._inc_stat("serpro/gazettes_future_skipped")
                continue

            # Somente após validação de ID, data e período, registra como visto
            self.seen_pub_ids.add(str_pub_id)
            new_valid_ids_count += 1
            self._inc_stat("serpro/gazettes_found")

            edition_number = self._extract_edition_number(title) or self._extract_edition_number(summary)
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
                self._inc_stat("serpro/stop_no_progress")
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

        # Define o índice da próxima página (se houver)
        next_page_start_index = None
        if not hit_date_cutoff and (start_index + self.PAGE_SIZE) < total_count:
            next_page_start_index = start_index + self.PAGE_SIZE

        # Inverte o lote para permitir consumo O(1) via list.pop()
        valid_items_batch.reverse()

        # Inicia a cadeia sequencial: emite apenas 1 requisição de download
        first_req = self._dispatch_next_download_or_page(
            remaining_items=valid_items_batch,
            next_page_start_index=next_page_start_index,
            module_version=module_version,
            csrf_token=csrf_token,
        )
        if first_req:
            yield first_req

    def _dispatch_next_download_or_page(
        self,
        remaining_items: list[dict[str, Any]],
        next_page_start_index: Optional[int],
        module_version: str,
        csrf_token: str,
    ) -> Optional[scrapy.Request]:
        """
        Dispara estritamente UMA requisição por vez:
        - Se ainda houver publicações no lote atual, requisita o próximo PDF;
        - Se o lote atual acabou, requisita a próxima página da listagem.
        """
        if remaining_items:
            item = remaining_items.pop()
            pub_id = item["pub_id"]

            download_url = (
                f"{self.BASE_URL}/screenservices/GovBRCidades_DOE/DoeConsultaCidadao/"
                f"DOEConsultaCidadao/ActionBuscaArquivoPublicacao"
                f"?{self.DEFAULT_API_VERSION_DOWNLOAD}"
            )
            download_payload = {
                "versionInfo": {
                    "moduleVersion": module_version,
                    "apiVersion": self.DEFAULT_API_VERSION_DOWNLOAD,
                },
                "viewName": "DoeConsultaCidadao.DOEConsultaCidadao",
                "screenData": {
                    "variables": {
                        "PublicacaoId": int(pub_id),
                        "Hash": self.HASH_PREFEITURA,
                    }
                },
            }

            gazette_meta = {
                "pub_id": pub_id,
                "date": item["date"],
                "edition_number": item["edition_number"],
                "is_extra_edition": item["is_extra_edition"],
                "power": self.power,
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
            self._inc_stat("serpro/download_rejected_too_large")
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
            self._inc_stat("serpro/download_json_errors")
            b64_content = None

        if not b64_content or not isinstance(b64_content, str):
            self.logger.warning(
                f"Publicação #{pub_id} de {meta.get('date')} não retornou conteúdo Base64 válido."
            )
            self._inc_stat("serpro/download_empty_base64")
        elif len(b64_content) > self.MAX_PDF_B64_CHARS:
            # Proteção contra PDF Gigante (após JSON)
            self.logger.error(
                f"[Teto de RAM Ativado] Publicação #{pub_id} ({len(b64_content)} chars > {self.MAX_PDF_B64_CHARS}) descartada para proteger a memória."
            )
            self._inc_stat("serpro/download_rejected_too_large")
        else:
            # Emite o Gazette para o pipeline com Data URI
            pdf_data_uri = f"data:application/pdf;base64,{b64_content}"
            self._inc_stat("serpro/gazettes_downloaded")

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
        self._inc_stat("serpro/download_network_failures")

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
        self._inc_stat("serpro/network_failures")

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
