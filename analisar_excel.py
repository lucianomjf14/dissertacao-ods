#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar todas as abas do arquivo Excel da dissertação
"""

import pandas as pd
import os

def analisar_excel(arquivo_excel):
    """
    Analisa todas as abas de um arquivo Excel e retorna informações detalhadas
    """
    try:
        # Ler o arquivo Excel
        xl_file = pd.ExcelFile(arquivo_excel)
        
        print(f"📊 ANÁLISE DO ARQUIVO: {os.path.basename(arquivo_excel)}")
        print("=" * 80)
        
        # Listar todas as abas
        print(f"🔍 TOTAL DE ABAS ENCONTRADAS: {len(xl_file.sheet_names)}\n")
        
        resultados = {}
        
        for i, aba in enumerate(xl_file.sheet_names, 1):
            print(f"📋 ABA {i}: '{aba}'")
            print("-" * 50)
            
            try:
                # Ler a aba
                df = pd.read_excel(arquivo_excel, sheet_name=aba)
                
                # Informações básicas
                linhas, colunas = df.shape
                print(f"   📏 Dimensões: {linhas} linhas × {colunas} colunas")
                
                # Colunas disponíveis
                print(f"   📂 Colunas ({len(df.columns)}):")
                for j, col in enumerate(df.columns, 1):
                    tipo_dados = str(df[col].dtype)
                    valores_nao_nulos = df[col].notna().sum()
                    print(f"      {j:2d}. {col} ({tipo_dados}) - {valores_nao_nulos} valores")
                
                # Verificar se há dados vazios
                celulas_vazias = df.isnull().sum().sum()
                total_celulas = linhas * colunas
                percentual_preenchido = ((total_celulas - celulas_vazias) / total_celulas * 100) if total_celulas > 0 else 0
                
                print(f"   📈 Preenchimento: {percentual_preenchido:.1f}% ({total_celulas - celulas_vazias}/{total_celulas} células)")
                
                # Primeiras linhas para exemplo (apenas colunas principais)
                if not df.empty:
                    print(f"   🔍 Primeiras linhas (amostra):")
                    # Mostrar apenas as 3 primeiras colunas para não poluir
                    cols_amostra = df.columns[:min(3, len(df.columns))]
                    amostra = df[cols_amostra].head(2)
                    for idx, row in amostra.iterrows():
                        valores = [str(val)[:30] + "..." if len(str(val)) > 30 else str(val) for val in row.values]
                        print(f"      Linha {idx + 1}: {valores}")
                
                # Salvar informações para retorno
                resultados[aba] = {
                    'linhas': linhas,
                    'colunas': colunas,
                    'colunas_nomes': list(df.columns),
                    'percentual_preenchido': percentual_preenchido,
                    'tipos_dados': {col: str(df[col].dtype) for col in df.columns}
                }
                
            except Exception as e:
                print(f"   ❌ Erro ao ler aba '{aba}': {str(e)}")
                resultados[aba] = {'erro': str(e)}
            
            print()
        
        # Resumo final
        print("📊 RESUMO GERAL")
        print("=" * 50)
        abas_validas = [aba for aba, info in resultados.items() if 'erro' not in info]
        total_linhas = sum(info['linhas'] for info in resultados.values() if 'linhas' in info)
        
        print(f"✅ Abas válidas: {len(abas_validas)} de {len(xl_file.sheet_names)}")
        print(f"📊 Total de linhas de dados: {total_linhas}")
        print(f"📋 Abas por tamanho:")
        
        # Ordenar abas por número de linhas
        abas_ordenadas = sorted(
            [(aba, info) for aba, info in resultados.items() if 'linhas' in info],
            key=lambda x: x[1]['linhas'],
            reverse=True
        )
        
        for aba, info in abas_ordenadas:
            print(f"   • {aba}: {info['linhas']} linhas × {info['colunas']} colunas")
        
        return resultados
        
    except Exception as e:
        print(f"❌ Erro ao analisar arquivo: {str(e)}")
        return None

if __name__ == "__main__":
    arquivo = "Análise de Conteúdo - Luciano 22_06.xlsx"
    
    if os.path.exists(arquivo):
        resultados = analisar_excel(arquivo)
    else:
        print(f"❌ Arquivo não encontrado: {arquivo}")
