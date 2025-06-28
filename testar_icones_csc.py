#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar os ícones dos Pilares CSC
"""

import pandas as pd
import json

def testar_icones_csc():
    print("🔍 TESTE DOS ÍCONES DOS PILARES CSC")
    print("=" * 50)
    
    # Carregar dados
    df = pd.read_excel('Análise de Conteúdo - Luciano 22_06.xlsx')
    
    print("📊 ANÁLISE DA COLUNA 'Pilar CSC':")
    print("-" * 30)
    
    # Verificar valores únicos
    valores_unicos = df['Pilar CSC'].value_counts()
    print(f"Total de valores únicos: {len(valores_unicos)}")
    print(f"Total de registros: {len(df)}")
    print()
    
    # Extrair todas as siglas
    todas_siglas = set()
    for valor in df['Pilar CSC'].dropna():
        siglas = [s.strip() for s in str(valor).split(',')]
        todas_siglas.update(siglas)
    
    # Remover valores vazios
    todas_siglas = {s for s in todas_siglas if s and s != '-'}
    
    print(f"🎯 SIGLAS ENCONTRADAS ({len(todas_siglas)}):")
    for sigla in sorted(todas_siglas):
        freq = sum(1 for valor in df['Pilar CSC'].dropna() 
                  if sigla in str(valor).split(','))
        print(f"  {sigla}: {freq} ocorrências")
    
    print("\n🗂️ MAPEAMENTO ESPERADO:")
    mapeamento = {
        'ECO': 'Economia',
        'EDU': 'Educação', 
        'EMP': 'Empreendedorismo',
        'ENE': 'Energia',
        'GOV': 'Governança',
        'MAM': 'Meio Ambiente',
        'MOB': 'Mobilidade',
        'SAU': 'Saúde',
        'SEG': 'Segurança',
        'TIC': 'Tecnologia e Inovação',
        'URB': 'Urbanismo'
    }
    
    for sigla in sorted(todas_siglas):
        nome_completo = mapeamento.get(sigla, '❌ NÃO MAPEADO')
        print(f"  {sigla} → {nome_completo}")
    
    # Verificar se existem siglas não mapeadas
    nao_mapeadas = todas_siglas - set(mapeamento.keys())
    if nao_mapeadas:
        print(f"\n⚠️ SIGLAS NÃO MAPEADAS: {nao_mapeadas}")
    else:
        print(f"\n✅ TODAS AS SIGLAS ESTÃO MAPEADAS!")
    
    print("\n📋 PRIMEIROS 10 REGISTROS COM PILARES:")
    for i, row in df.head(10).iterrows():
        if pd.notna(row['Pilar CSC']) and row['Pilar CSC'] != '-':
            print(f"ID {row['ID']}: {row['Pilar CSC']}")
      # Salvar dados para análise
    resultado = {
        'siglas_encontradas': list(sorted(todas_siglas)),
        'mapeamento': mapeamento,
        'valores_unicos': {k: int(v) for k, v in valores_unicos.head(10).items()},
        'total_registros': int(len(df)),
        'registros_com_pilares': int(len(df[df['Pilar CSC'].notna() & (df['Pilar CSC'] != '-')]))
    }
    
    with open('teste_icones_csc.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultado salvo em 'teste_icones_csc.json'")

if __name__ == "__main__":
    testar_icones_csc()
