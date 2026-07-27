#!/usr/bin/env python
"""
Script para testar o fatiamento de PDF por município.
"""
import os
from gazette.utils.pdf_utils import extract_municipalities_from_pdf, split_pdf_by_municipalities
from gazette.utils.territory_mapping import match_municipalities_from_summary, get_cached_sc_municipalities

def test_pdf_splitting():
    pdf_path = '/home/grisolfi/Dev/querido-diario/data_collection/gazette/spiders/base/1768412435_edicao_5040_assinada.pdf'
    
    print("="*70)
    print("TESTE DE FATIAMENTO DE PDF POR MUNICÍPIO")
    print("="*70)
    
    # 1. Extrair municípios do sumário
    print("\n1. Extraindo municípios do sumário...")
    municipalities_pages = extract_municipalities_from_pdf(pdf_path)
    print(f"   Municípios encontrados: {len(municipalities_pages)}")
    
    # 2. Mapear para códigos IBGE
    print("\n2. Mapeando municípios para códigos IBGE...")
    sc_territories = get_cached_sc_municipalities()
    matched, not_found = match_municipalities_from_summary(
        list(municipalities_pages.keys()),
        sc_territories
    )
    
    print(f"   Mapeados com sucesso: {len(matched)}")
    print(f"   Não encontrados: {len(not_found)}")
    
    if not_found:
        print(f"\n   Municípios não encontrados:")
        for mun in not_found[:10]:  # Mostrar apenas os primeiros 10
            print(f"     - {mun}")
        if len(not_found) > 10:
            print(f"     ... e mais {len(not_found) - 10}")
    
    # 3. Fatiar PDF (apenas os primeiros 5 para teste)
    print("\n3. Fatiando PDF (testando com primeiros 5 municípios CONSECUTIVOS)...")
    
    # Pegar apenas os 5 primeiros municípios ORDENADOS POR PÁGINA para teste
    sorted_all = sorted(municipalities_pages.items(), key=lambda x: x[1])
    test_municipalities = dict(sorted_all[:5])
    
    temp_dir = "/tmp/ciga_sc_test"
    os.makedirs(temp_dir, exist_ok=True)
    
    results = split_pdf_by_municipalities(
        pdf_path,
        test_municipalities,
        temp_dir=temp_dir,
        save_to_disk=True
    )
    
    print(f"\n   PDFs gerados em: {temp_dir}")
    print(f"\n   Resultados:")
    for municipality, start_page, end_page, pdf_bytes in results:
        territory_id = matched.get(municipality, "???")
        size_kb = len(pdf_bytes) / 1024
        pages_count = end_page - start_page + 1
        print(f"     • {municipality:30s} [{territory_id}]")
        print(f"       Páginas {start_page:4d}-{end_page:4d} ({pages_count:3d} páginas, {size_kb:7.1f} KB)")
    
    print("\n" + "="*70)
    print("TESTE CONCLUÍDO COM SUCESSO!")
    print("="*70)
    print(f"\nArquivos salvos em: {temp_dir}")
    print("Você pode abrir os PDFs para verificar se foram fatiados corretamente.")

if __name__ == "__main__":
    test_pdf_splitting()
