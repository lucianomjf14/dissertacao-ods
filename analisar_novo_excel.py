#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise do novo arquivo Excel: Analise_41_Estudos_Cidades_Inteligentes.xlsx
"""

import pandas as pd
import json

def analisar_novo_excel():
    print("🔍 ANÁLISE DO NOVO ARQUIVO EXCEL")
    print("=" * 50)
    
    # Carregar dados
    df = pd.read_excel('Analise_41_Estudos_Cidades_Inteligentes.xlsx')
    
    print(f"📊 DIMENSÕES: {len(df)} linhas x {len(df.columns)} colunas")
    print(f"📋 COLUNAS: {list(df.columns)}")
    print()
    
    # Analisar cada linha
    print("📝 DADOS POR ESTUDO:")
    print("-" * 50)
    
    for i, row in df.iterrows():
        print(f"ID {row['ID']}:")
        print(f"  Palavras-Chave: {row['Palavras-Chave']}")
        print(f"  Nº Palavras: {row['Nº Palavras-Chave']}")
        print(f"  Indicadores: {row['Indicadores Únicos']}")
        print(f"  Eixos: {row['Eixos Relacionados']}")
        print(f"  Nº Eixos: {row['Nº Eixos']}")
        print()
    
    # Análise estatística
    print("📈 ESTATÍSTICAS GERAIS:")
    print("-" * 30)
    print(f"Total de estudos: {len(df)}")
    print(f"Média de palavras-chave por estudo: {df['Nº Palavras-Chave'].mean():.1f}")
    print(f"Média de eixos por estudo: {df['Nº Eixos'].mean():.1f}")
    
    # Análise de palavras-chave
    todas_palavras = []
    for palavras_str in df['Palavras-Chave']:
        if pd.notna(palavras_str):
            palavras = [p.strip() for p in str(palavras_str).split(';')]
            todas_palavras.extend(palavras)
    
    # Contar frequências
    from collections import Counter
    contagem_palavras = Counter(todas_palavras)
    
    print(f"\nTotal de palavras-chave: {len(todas_palavras)}")
    print(f"Palavras-chave únicas: {len(contagem_palavras)}")
    
    print("\n🏆 TOP 20 PALAVRAS-CHAVE:")
    for i, (palavra, freq) in enumerate(contagem_palavras.most_common(20), 1):
        print(f"{i:2d}. {palavra} ({freq}x)")
    
    # Análise de eixos
    todos_eixos = []
    for eixos_str in df['Eixos Relacionados']:
        if pd.notna(eixos_str):
            eixos = [e.strip() for e in str(eixos_str).split(',')]
            todos_eixos.extend(eixos)
    
    contagem_eixos = Counter(todos_eixos)
    
    print(f"\n🎯 EIXOS CSC MAIS FREQUENTES:")
    for i, (eixo, freq) in enumerate(contagem_eixos.most_common(), 1):
        print(f"{i:2d}. {eixo} ({freq}x)")
    
    # Salvar análise em JSON
    analise = {
        'dimensoes': {
            'linhas': len(df),
            'colunas': len(df.columns)
        },
        'colunas': list(df.columns),
        'estatisticas': {
            'total_estudos': len(df),
            'media_palavras_chave': float(df['Nº Palavras-Chave'].mean()),
            'media_eixos': float(df['Nº Eixos'].mean()),
            'total_palavras_chave': len(todas_palavras),
            'palavras_chave_unicas': len(contagem_palavras)
        },
        'top_palavras_chave': dict(contagem_palavras.most_common(20)),
        'eixos_csc': dict(contagem_eixos)
    }
    
    with open('analise_novo_excel.json', 'w', encoding='utf-8') as f:
        json.dump(analise, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Análise salva em 'analise_novo_excel.json'")

if __name__ == "__main__":
    analisar_novo_excel()
