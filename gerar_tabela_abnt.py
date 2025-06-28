#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar tabela em formato ABNT a partir de arquivo Excel
Destinado para apêndice de dissertação de mestrado
"""

import pandas as pd
import sys
from pathlib import Path

def ler_excel_e_gerar_tabela_abnt(caminho_arquivo):
    """
    Lê arquivo Excel e gera tabela formatada em ABNT
    """
    try:
        # Lê o arquivo Excel
        print(f"Lendo arquivo: {caminho_arquivo}")
        
        # Tenta ler todas as planilhas
        xl_file = pd.ExcelFile(caminho_arquivo)
        print(f"Planilhas encontradas: {xl_file.sheet_names}")
        
        # Lê a primeira planilha (ou você pode especificar qual planilha ler)
        df = pd.read_excel(caminho_arquivo, sheet_name=0)
        
        print(f"Dimensões dos dados: {df.shape[0]} linhas x {df.shape[1]} colunas")
        print(f"Colunas: {list(df.columns)}")
        
        # Mostra as primeiras linhas para entender a estrutura
        print("\n=== PRIMEIRAS 10 LINHAS DOS DADOS ===")
        print(df.head(10))
        
        # Informações sobre dados faltantes
        print(f"\n=== INFORMAÇÕES SOBRE DADOS FALTANTES ===")
        print(df.isnull().sum())
        
        return df, xl_file.sheet_names
        
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None, None

def gerar_codigo_latex_tabela_abnt(df, titulo_tabela="Análise de Conteúdo", fonte="Elaborado pelo autor"):
    """
    Gera código LaTeX para tabela em formato ABNT
    """
    
    # Limita o número de colunas se necessário (LaTeX tem limitações)
    max_cols = 6
    if len(df.columns) > max_cols:
        print(f"Aviso: Tabela tem {len(df.columns)} colunas. Mostrando apenas as primeiras {max_cols}.")
        df_display = df.iloc[:, :max_cols]
    else:
        df_display = df
    
    # Remove linhas completamente vazias
    df_display = df_display.dropna(how='all')
    
    # Limita o número de linhas para tabela de exemplo
    max_rows = 20
    if len(df_display) > max_rows:
        print(f"Aviso: Tabela tem {len(df_display)} linhas. Mostrando apenas as primeiras {max_rows}.")
        df_display = df_display.head(max_rows)
    
    # Substitui valores NaN por texto em branco
    df_display = df_display.fillna("")
    
    # Gera o código LaTeX
    latex_code = f"""\\begin{{table}}[htbp]
\\centering
\\caption{{{titulo_tabela}}}
\\label{{tab:analise_conteudo}}
\\begin{{tabular}}{{|{'l|' * len(df_display.columns)}}}
\\hline
"""
    
    # Cabeçalho
    headers = [str(col).replace('_', '\\_').replace('&', '\\&') for col in df_display.columns]
    latex_code += " & ".join([f"\\textbf{{{header}}}" for header in headers]) + " \\\\\n\\hline\n"
    
    # Linhas de dados
    for _, row in df_display.iterrows():
        row_data = []
        for item in row:
            # Converte para string e escapa caracteres especiais do LaTeX
            item_str = str(item).replace('_', '\\_').replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')
            # Limita o tamanho do texto se for muito longo
            if len(item_str) > 50:
                item_str = item_str[:47] + "..."
            row_data.append(item_str)
        
        latex_code += " & ".join(row_data) + " \\\\\n\\hline\n"
    
    latex_code += f"""\\end{{tabular}}
\\\\[0.2cm]
{{\\footnotesize Fonte: {fonte}}}
\\end{{table}}"""
    
    return latex_code

def main():
    # Caminho do arquivo Excel
    caminho_excel = r"C:\Users\lucia\Dissertação\Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx"
    
    # Verifica se o arquivo existe
    if not Path(caminho_excel).exists():
        print(f"Erro: Arquivo não encontrado em {caminho_excel}")
        return
    
    # Lê o arquivo Excel
    df, sheet_names = ler_excel_e_gerar_tabela_abnt(caminho_excel)
    
    if df is not None:
        print("\n" + "="*80)
        print("CÓDIGO LATEX PARA TABELA EM FORMATO ABNT")
        print("="*80)
        
        # Gera o código LaTeX
        latex_code = gerar_codigo_latex_tabela_abnt(
            df, 
            titulo_tabela="Análise de Conteúdo com Corpus Corrigido",
            fonte="Elaborado pelo autor (2025)"
        )
        
        print(latex_code)
        
        # Salva o código em arquivo
        with open(r"C:\Users\lucia\Dissertação\tabela_abnt.tex", "w", encoding="utf-8") as f:
            f.write(latex_code)
        
        print(f"\n=== ARQUIVO SALVO ===")
        print(f"Código LaTeX salvo em: C:\\Users\\lucia\\Dissertação\\tabela_abnt.tex")
        
        # Gera também uma versão em formato de texto simples
        print("\n" + "="*80)
        print("VERSÃO EM TEXTO SIMPLES (PREVIEW)")
        print("="*80)
        
        # Mostra uma versão simplificada em texto
        df_preview = df.head(10) if len(df) > 10 else df
        print(df_preview.to_string(index=False))
        
    else:
        print("Não foi possível processar o arquivo Excel.")

if __name__ == "__main__":
    main()
