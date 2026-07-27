import os
import re
import tempfile
from datetime import datetime
from urllib.parse import urlencode

import scrapy
from scrapy.exceptions import NotConfigured

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.pdf_utils import (
    extract_municipalities_from_pdf,
    split_pdf_by_municipalities
)
from gazette.utils.territory_mapping import (
    match_municipalities_from_summary,
    get_cached_sc_territories
)


class BaseCigaSCSpider(BaseGazetteSpider):
    """
    Base Spider for municipalities using CIGA/SC (Consórcio de Inovação na 
    Gestão Pública de Santa Catarina) platform.
    
    The CIGA/SC platform is used by municipalities in Santa Catarina to publish
    their official gazettes. This spider navigates the paginated listing of 
    gazette editions and downloads PDFs for the specified date range.
    
    Website: https://edicao.dom.sc.gov.br/
    
    Attributes
    ----------
    municipality_id : str
        The municipality ID in the CIGA/SC system. Use "-1" for "Edição Geral"
        (general edition with all municipalities) or specific municipality IDs.
        Must be defined in child classes.
    """

    allowed_domains = ["edicao.dom.sc.gov.br", "diariomunicipal.sc.gov.br"]
    base_url = "https://edicao.dom.sc.gov.br/"
    
    # Diretório para salvar PDFs temporários durante desenvolvimento/debug
    temp_dir_base = "/tmp/ciga_sc_split"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "municipality_id"):
            raise NotConfigured("Please set a value for `municipality_id`")
        
        # Flag para indicar se deve fatiar PDFs (apenas para Edição Geral)
        self.split_pdf = self.municipality_id == "-1"
        
        # Carregar territórios de SC uma vez
        if self.split_pdf:
            self.sc_territories = get_cached_sc_territories()
        
        super(BaseCigaSCSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        """
        Generate requests for all pages. The site uses pagination with parameter
        Edicao_page starting from 1.
        """
        # Start with the first page to determine total pages
        yield scrapy.Request(
            self._build_url(page=1),
            callback=self.parse_gazette_list,
            meta={"page": 1},
        )

    def _build_url(self, page=1):
        """
        Build the URL with query parameters for municipality and pagination.
        
        Note: The API does not support date filtering via parameters.
        Results are returned in descending date order (newest first).
        We filter client-side in parse_gazette_list().
        
        Parameters
        ----------
        page : int
            The page number (starts at 1)
        """
        params = {
            "r": "site/edicoes",
            "Edicao[cod_municipio]": self.municipality_id,
            "Edicao_page": page,
        }
        
        return f"{self.base_url}?{urlencode(params)}"

    def parse_gazette_list(self, response):
        """
        Parse the gazette listing page and extract gazette information from the table.
        
        For "Edição Geral" (municipality_id == "-1"), downloads the PDF and splits
        it by municipality. For specific municipalities, works normally.
        """
        current_page = response.meta.get("page", 1)
        found_gazettes = False
        
        # Extract gazette rows from the table
        for row in response.css("table.items tbody tr"):
            # Extract data from table cells
            cells = row.css("td")
            
            if len(cells) < 6:
                continue
            
            # Parse gazette information
            municipality_name = cells[0].css("::text").get(default="").strip()
            edition_number = cells[1].css("::text").get(default="").strip()
            date_text = cells[2].css("::text").get(default="").strip()
            publications_count = cells[3].css("::text").get(default="").strip()
            file_size = cells[4].css("::text").get(default="").strip()
            
            # Extract PDF URL from the download link
            pdf_url = cells[5].css("a[title='Baixar']::attr(href)").get()
            
            if not pdf_url or not date_text:
                continue
            
            # Parse date from format DD/MM/YYYY
            try:
                gazette_date = datetime.strptime(date_text, "%d/%m/%Y").date()
            except ValueError:
                self.logger.warning(f"Could not parse date: {date_text}")
                continue
            
            # Check if date is in range (client-side filtering)
            # Pages are ordered by date descending (newest first)
            if gazette_date < self.start_date:
                # Reached dates before our range, stop pagination
                self.logger.info(
                    f"Reached date {gazette_date} which is before start_date "
                    f"{self.start_date}. Stopping pagination."
                )
                return
            
            if gazette_date > self.end_date:
                # Skip this gazette but continue to next ones
                self.logger.debug(
                    f"Skipping date {gazette_date} (after end_date {self.end_date})"
                )
                continue
            
            found_gazettes = True
            
            # Check if it's an extra edition by looking at the PDF filename
            is_extra = "_EXTRA_" in pdf_url or "EXTRA" in pdf_url.upper()
            
            # If this is the "Edição Geral" (all municipalities), download and split
            if self.split_pdf:
                self.logger.info(
                    f"Found Edição Geral for {gazette_date}. "
                    f"Will download and split by municipality."
                )
                yield scrapy.Request(
                    pdf_url,
                    callback=self.parse_and_split_pdf,
                    meta={
                        'date': gazette_date,
                        'edition_number': edition_number,
                        'is_extra': is_extra,
                        'file_size': file_size,
                        'publications_count': publications_count
                    }
                )
            else:
                # Single municipality: normal behavior
                yield Gazette(
                    date=gazette_date,
                    edition_number=edition_number,
                    file_urls=[pdf_url],
                    is_extra_edition=is_extra,
                    power="executive_legislative",
                )
        
        # Follow next page using Scrapy's standard pagination pattern
        # The yiiPager framework disables the 'next' button on last page
        next_page_link = response.css(
            "ul.yiiPager li.next:not(.disabled) a::attr(href)"
        ).get()
        
        if next_page_link:
            current_page = response.meta.get("page", 1)
            self.logger.info(
                f"Following pagination: page {current_page} -> {current_page + 1} "
                f"(processed {found_gazettes} gazettes on current page)"
            )
            yield response.follow(next_page_link, callback=self.parse_gazette_list)
        else:
            self.logger.info(
                f"Pagination complete at page {response.meta.get('page', 1)} "
                f"(no next page link found, processed {found_gazettes} gazettes on last page)"
            )
    
    def parse_and_split_pdf(self, response):
        """
        Downloads the "Edição Geral" PDF, extracts the summary of municipalities,
        splits the PDF by municipality, and yields one Gazette item per municipality.
        
        This method is only called when processing the "Edição Geral".
        """
        gazette_date = response.meta['date']
        edition_number = response.meta['edition_number']
        is_extra = response.meta['is_extra']
        
        self.logger.info(
            f"Processing Edição Geral #{edition_number} from {gazette_date}. "
            f"PDF size: {len(response.body) / 1024 / 1024:.1f} MB"
        )
        
        # Save PDF temporarily for processing
        temp_dir = os.path.join(self.temp_dir_base, f"{gazette_date}_{edition_number}")
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_pdf_path = os.path.join(temp_dir, f"edicao_{edition_number}_full.pdf")
        with open(temp_pdf_path, 'wb') as f:
            f.write(response.body)
        
        try:
            # Step 1: Extract municipalities from summary
            self.logger.info("Step 1: Extracting municipalities from PDF summary...")
            municipalities_pages = extract_municipalities_from_pdf(temp_pdf_path)
            self.logger.info(f"Found {len(municipalities_pages)} municipalities in summary")
            
            # Step 2: Map municipality names to territory IDs
            self.logger.info("Step 2: Mapping municipalities to territory IDs...")
            matched, not_found = match_municipalities_from_summary(
                list(municipalities_pages.keys()),
                self.sc_territories
            )
            
            self.logger.info(f"Mapped {len(matched)} municipalities successfully")
            if not_found:
                self.logger.warning(
                    f"Could not map {len(not_found)} municipalities: {', '.join(not_found[:5])}"
                    f"{'...' if len(not_found) > 5 else ''}"
                )
            
            # Step 3: Split PDF by municipality
            self.logger.info("Step 3: Splitting PDF by municipality...")
            split_results = split_pdf_by_municipalities(
                temp_pdf_path,
                municipalities_pages,
                temp_dir=temp_dir,
                save_to_disk=False  # Don't save with temp format - we save below with proper format
            )
            
            self.logger.info(f"Successfully split PDF into {len(split_results)} files")
            
            # Step 4: Yield one Gazette item per municipality
            for municipality_name, start_page, end_page, pdf_bytes in split_results:
                territory_id = matched.get(municipality_name)
                
                if not territory_id:
                    self.logger.warning(
                        f"Skipping {municipality_name} (pages {start_page}-{end_page}): "
                        f"no territory ID found"
                    )
                    continue
                
                # Create a unique filename for this municipality's PDF
                safe_name = re.sub(r'[^\w\s-]', '', municipality_name).strip().replace(' ', '_')
                municipality_filename = f"{territory_id}_{gazette_date}_{edition_number}.pdf"
                
                # Save the split PDF
                municipality_pdf_path = os.path.join(temp_dir, municipality_filename)
                with open(municipality_pdf_path, 'wb') as f:
                    f.write(pdf_bytes)
                
                # Yield Gazette item with the file:// URL for local files
                # The pipeline will handle uploading to S3
                file_url = f"file://{os.path.abspath(municipality_pdf_path)}"
                
                yield Gazette(
                    date=gazette_date,
                    edition_number=edition_number,
                    territory_id=territory_id,
                    file_urls=[file_url],  # Use file:// scheme for local files
                    is_extra_edition=is_extra,
                    power="executive_legislative",
                    scraped_at=datetime.utcnow(),
                )
                
                self.logger.debug(
                    f"✓ {municipality_name} [{territory_id}]: "
                    f"pages {start_page}-{end_page} "
                    f"({end_page - start_page + 1} pages, "
                    f"{len(pdf_bytes) / 1024:.1f} KB)"
                )
            
            self.logger.info(
                f"✓ Completed processing Edição Geral #{edition_number}: "
                f"generated {len(split_results)} gazette files"
            )
            
        except Exception as e:
            self.logger.error(
                f"Error processing Edição Geral #{edition_number}: {e}",
                exc_info=True
            )
        finally:
            # Clean up the full PDF (keep split PDFs for debugging)
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
                self.logger.debug(f"Cleaned up temporary file: {temp_pdf_path}")
