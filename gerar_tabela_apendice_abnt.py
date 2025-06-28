#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar tabela aprimorada em formato ABNT para apêndice de dissertação
Incluindo mais colunas relevantes da análise de conteúdo
"""

import pandas as pd
from pathlib import Path

def gerar_tabela_abnt_completa(caminho_arquivo):
    """
    Gera uma tabela ABNT mais completa com informações relevantes para dissertação
    """
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(caminho_arquivo, sheet_name=0)
        
        # Seleciona colunas mais relevantes para o apêndice
        colunas_relevantes = ['ID', 'Autores', 'Título', 'Ano', 'Periódico', 'ODS (Geral / Específico)', 'Aspecto Principal - Estudo']
        
        # Verifica se as colunas existem
        colunas_existentes = [col for col in colunas_relevantes if col in df.columns]
        df_tabela = df[colunas_existentes].copy()
        
        # Remove linhas completamente vazias
        df_tabela = df_tabela.dropna(how='all')
        
        # Substitui valores NaN por texto em branco
        df_tabela = df_tabela.fillna("")
        
        # Trunca títulos muito longos
        if 'Título' in df_tabela.columns:
            df_tabela['Título'] = df_tabela['Título'].apply(lambda x: str(x)[:60] + "..." if len(str(x)) > 60 else str(x))
        
        # Trunca nomes de periódicos muito longos
        if 'Periódico' in df_tabela.columns:
            df_tabela['Periódico'] = df_tabela['Periódico'].apply(lambda x: str(x)[:30] + "..." if len(str(x)) > 30 else str(x))
        
        # Trunca aspectos principais muito longos
        if 'Aspecto Principal - Estudo' in df_tabela.columns:
            df_tabela['Aspecto Principal - Estudo'] = df_tabela['Aspecto Principal - Estudo'].apply(lambda x: str(x)[:40] + "..." if len(str(x)) > 40 else str(x))
        
        return df_tabela
        
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        return None

def gerar_latex_tabela_apendice(df):
    """
    Gera código LaTeX para tabela de apêndice em formato ABNT
    """
    
    # Configuração da tabela
    num_cols = len(df.columns)
    col_spec = "|" + "p{2cm}|" * num_cols  # Colunas com largura fixa
    
    latex_code = f"""\\begin{{table}}[htbp]
\\centering
\\caption{{Corpus da Análise de Conteúdo - Artigos Selecionados}}
\\label{{tab:corpus_analise_conteudo}}
\\footnotesize
\\begin{{tabular}}{{{col_spec}}}
\\hline
"""
    
    # Cabeçalho
    headers = []
    for col in df.columns:
        header = str(col).replace('_', '\\_').replace('&', '\\&').replace('ODS (Geral / Específico)', 'ODS')
        headers.append(f"\\textbf{{{header}}}")
    
    latex_code += " & ".join(headers) + " \\\\\n\\hline\n"
    
    # Linhas de dados
    for _, row in df.iterrows():
        row_data = []
        for item in row:
            # Converte para string e escapa caracteres especiais do LaTeX
            item_str = str(item).replace('_', '\\_').replace('&', '\\&').replace('%', '\\%').replace('$', '\\$').replace('#', '\\#')
            row_data.append(item_str)
        
        latex_code += " & ".join(row_data) + " \\\\\n\\hline\n"
    
    latex_code += f"""\\end{{tabular}}
\\\\[0.3cm]
{{\\footnotesize \\textbf{{Fonte:}} Elaborado pelo autor (2025).}}
\\end{{table}}"""
    
    return latex_code

def gerar_tabela_longitudinal(df):
    """
    Gera uma tabela longitudinal (formato retrato) para trabalhar melhor com muitas colunas
    """
    
    latex_code = """\\begin{longtable}{|p{1cm}|p{3cm}|p{6cm}|p{1cm}|p{3cm}|}
\\caption{Corpus da Análise de Conteúdo - Artigos Selecionados} \\label{tab:corpus_analise_conteudo_detalhado} \\\\
\\hline
\\textbf{ID} & \\textbf{Autores} & \\textbf{Título} & \\textbf{Ano} & \\textbf{Periódico} \\\\
\\hline
\\endfirsthead

\\multicolumn{5}{c}%
{\\tablename\\ \\thetable\\ -- \\textit{Continuação da página anterior}} \\\\
\\hline
\\textbf{ID} & \\textbf{Autores} & \\textbf{Título} & \\textbf{Ano} & \\textbf{Periódico} \\\\
\\hline
\\endhead

\\hline \\multicolumn{5}{r}{\\textit{Continua na próxima página}} \\\\
\\endfoot

\\hline
\\multicolumn{5}{l}{\\footnotesize \\textbf{Fonte:} Elaborado pelo autor (2025).} \\\\
\\endlastfoot

"""
    
    # Seleciona apenas as colunas principais
    colunas_principais = ['ID', 'Autores', 'Título', 'Ano', 'Periódico']
    
    for _, row in df.iterrows():
        linha_dados = []
        for col in colunas_principais:
            if col in df.columns:
                valor = str(row[col]).replace('_', '\\_').replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')
                if col == 'Título' and len(valor) > 80:
                    valor = valor[:77] + "..."
                elif col == 'Periódico' and len(valor) > 35:
                    valor = valor[:32] + "..."
                linha_dados.append(valor)
            else:
                linha_dados.append("")
        
        latex_code += " & ".join(linha_dados) + " \\\\\n\\hline\n"
    
    latex_code += "\\end{longtable}"
    
    return latex_code

def main():
    # Caminho do arquivo Excel
    caminho_excel = r"C:\Users\lucia\Dissertação\Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx"
    
    # Verifica se o arquivo existe
    if not Path(caminho_excel).exists():
        print(f"Erro: Arquivo não encontrado em {caminho_excel}")
        return
    
    # Processa o arquivo
    df = gerar_tabela_abnt_completa(caminho_excel)
    
    if df is not None:
        print("="*80)
        print("TABELA ABNT PARA APÊNDICE DE DISSERTAÇÃO")
        print("="*80)
        
        # Mostra informações sobre os dados
        print(f"Total de artigos: {len(df)}")
        print(f"Colunas incluídas: {list(df.columns)}")
        print(f"Anos cobertos: {df['Ano'].min() if 'Ano' in df.columns else 'N/A'} - {df['Ano'].max() if 'Ano' in df.columns else 'N/A'}")
        
        # Gera tabela compacta
        print("\n" + "="*80)
        print("TABELA COMPACTA (FORMATO PAISAGEM)")
        print("="*80)
        
        tabela_compacta = gerar_latex_tabela_apendice(df)
        print(tabela_compacta)
        
        # Salva tabela compacta
        with open(r"C:\Users\lucia\Dissertação\tabela_apendice_compacta.tex", "w", encoding="utf-8") as f:
            f.write(tabela_compacta)
        
        # Gera tabela longitudinal
        print("\n" + "="*80)
        print("TABELA LONGITUDINAL (FORMATO RETRATO)")
        print("="*80)
        
        tabela_longitudinal = gerar_tabela_longitudinal(df)
        print(tabela_longitudinal)
        
        # Salva tabela longitudinal
        with open(r"C:\Users\lucia\Dissertação\tabela_apendice_longitudinal.tex", "w", encoding="utf-8") as f:
            f.write(tabela_longitudinal)
        
        print(f"\n=== ARQUIVOS SALVOS ===")
        print(f"Tabela compacta: C:\\Users\\lucia\\Dissertação\\tabela_apendice_compacta.tex")
        print(f"Tabela longitudinal: C:\\Users\\lucia\\Dissertação\\tabela_apendice_longitudinal.tex")
        
        # Gera instruções de uso
        print(f"\n=== INSTRUÇÕES DE USO ===")
        print("1. Para a tabela compacta, adicione no preâmbulo do LaTeX:")
        print("   \\usepackage{array}")
        print("   \\usepackage{tabularx}")
        print("")
        print("2. Para a tabela longitudinal, adicione no preâmbulo do LaTeX:")
        print("   \\usepackage{longtable}")
        print("   \\usepackage{array}")
        print("")
        print("3. Insira o código no seu apêndice dentro do ambiente de documento.")
        print("4. Compile com pdflatex para melhor resultado.")
        
    else:
        print("Não foi possível processar o arquivo Excel.")

if __name__ == "__main__":
    main()
