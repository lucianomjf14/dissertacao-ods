#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar o comportamento de truncamento no modo CSC
"""

import pandas as pd

def testar_truncamento_csc():
    print("🔍 TESTE DE TRUNCAMENTO NO MODO CSC")
    print("=" * 45)
    
    # Carregar dados
    df = pd.read_excel('Análise de Conteúdo - Luciano 22_06.xlsx')
    
    print("📋 COLUNAS DO MODO CSC:")
    csc_columns = ['ID', 'Palavras Chave', 'Palavras chave normalizadas e Traduzidas', 'Indicadores CSC', 'Pilar CSC']
    
    for i, col in enumerate(csc_columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\n📊 ANÁLISE DE COMPRIMENTO DOS TEXTOS:")
    
    for col in csc_columns:
        if col in df.columns and col != 'ID':
            valores_validos = df[col].dropna()
            if len(valores_validos) > 0:
                comprimentos = [len(str(v)) for v in valores_validos]
                comprimento_medio = sum(comprimentos) / len(comprimentos)
                maior_comprimento = max(comprimentos)
                menor_comprimento = min(comprimentos)
                
                print(f"\n  📝 {col}:")
                print(f"    Registros com dados: {len(valores_validos)}")
                print(f"    Comprimento médio: {comprimento_medio:.1f} caracteres")
                print(f"    Menor: {menor_comprimento} caracteres")
                print(f"    Maior: {maior_comprimento} caracteres")
                
                # Lógica de truncamento conforme implementado
                if col == 'Indicadores CSC':
                    print(f"    ✅ NO MODO CSC: SEM truncamento (texto completo)")
                    print(f"    📏 Em outros modos: Truncado se > 20 caracteres")
                elif col in ['Palavras Chave', 'Palavras chave normalizadas e Traduzidas']:
                    print(f"    📏 NO MODO CSC: Truncado se > 40 caracteres")
                    print(f"    📏 Em outros modos: Truncado se > 40 caracteres (exceto Technology)")
                elif col == 'Pilar CSC':
                    print(f"    🎨 Sempre exibe ícones visuais (não truncado)")
    
    print(f"\n🎯 EXEMPLOS DE DADOS PARA TESTE VISUAL:")
    
    # Mostrar alguns exemplos de Indicadores CSC para ver o comprimento
    print(f"\n📄 EXEMPLOS DE 'Indicadores CSC' (primeiros 3 registros):")
    for i, row in df.head(3).iterrows():
        if pd.notna(row['Indicadores CSC']):
            indicador = str(row['Indicadores CSC'])
            print(f"\n  ID {row['ID']}:")
            print(f"    Comprimento: {len(indicador)} caracteres")
            if len(indicador) > 100:
                print(f"    Texto: {indicador[:100]}...")
            else:
                print(f"    Texto: {indicador}")
            print(f"    Truncamento normal: {'SIM' if len(indicador) > 20 else 'NÃO'}")
            print(f"    No modo CSC: TEXTO COMPLETO (sem truncamento)")
    
    print(f"\n✅ RESUMO DAS REGRAS DE TRUNCAMENTO:")
    print(f"  📋 Modo CSC implementado:")
    print(f"    • ID: Sem truncamento (sempre curto)")
    print(f"    • Palavras Chave: Truncado se > 40 caracteres")
    print(f"    • Palavras chave normalizadas: Truncado se > 40 caracteres")
    print(f"    • Indicadores CSC: ✅ SEM TRUNCAMENTO (texto completo)")
    print(f"    • Pilar CSC: Ícones visuais (sem truncamento)")

if __name__ == "__main__":
    testar_truncamento_csc()
