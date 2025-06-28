#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar correspondência entre links e colunas na tabela
"""

import pandas as pd
from pathlib import Path

def verificar_correspondencia_colunas(caminho_arquivo):
    """
    Verifica se os links correspondem corretamente às colunas
    """
    try:
        # Lê o arquivo Excel
        print("🔍 Verificando correspondência entre links e colunas...")
        df = pd.read_excel(caminho_arquivo, sheet_name=0)
        
        print(f"📊 Dados carregados: {df.shape[0]} linhas x {df.shape[1]} colunas")
        print(f"📋 Colunas encontradas: {list(df.columns)}")
        
        # Verifica as primeiras linhas para entender a estrutura
        print("\n" + "="*80)
        print("ANÁLISE DA ESTRUTURA DOS DADOS")
        print("="*80)
        
        # Mostra informações sobre cada coluna
        for i, col in enumerate(df.columns):
            print(f"\n🔹 Coluna {i}: '{col}'")
            
            # Mostra valores não nulos únicos (limitado a 3 exemplos)
            valores_nao_nulos = df[col].dropna()
            if len(valores_nao_nulos) > 0:
                exemplos = valores_nao_nulos.head(3).tolist()
                for j, exemplo in enumerate(exemplos):
                    exemplo_str = str(exemplo)
                    if len(exemplo_str) > 100:
                        exemplo_str = exemplo_str[:97] + "..."
                    print(f"   Exemplo {j+1}: {exemplo_str}")
            else:
                print("   (Sem dados válidos)")
        
        # Verificação específica dos links
        print("\n" + "="*80)
        print("VERIFICAÇÃO DOS LINKS")
        print("="*80)
        
        if 'Link' in df.columns:
            links = df['Link'].dropna()
            print(f"📎 Total de links encontrados: {len(links)}")
            
            # Analisa os primeiros 5 links
            print("\n🔗 Primeiros 5 links:")
            for i, link in enumerate(links.head(5)):
                print(f"   {i+1}. {link}")
            
            # Verifica se há padrões nos links
            dominios = {}
            for link in links:
                if isinstance(link, str) and link.startswith('http'):
                    dominio = link.split('/')[2] if len(link.split('/')) > 2 else 'desconhecido'
                    dominios[dominio] = dominios.get(dominio, 0) + 1
            
            print(f"\n📈 Distribuição por domínio:")
            for dominio, count in sorted(dominios.items(), key=lambda x: x[1], reverse=True):
                print(f"   {dominio}: {count} links")
        
        # Verificação da correspondência linha por linha
        print("\n" + "="*80)
        print("VERIFICAÇÃO LINHA POR LINHA (Primeiras 5 linhas)")
        print("="*80)
        
        for i in range(min(5, len(df))):
            print(f"\n📄 LINHA {i+1}:")
            for col in df.columns:
                valor = df.iloc[i][col]
                if pd.notna(valor):
                    valor_str = str(valor)
                    if len(valor_str) > 80:
                        valor_str = valor_str[:77] + "..."
                    print(f"   {col}: {valor_str}")
                else:
                    print(f"   {col}: (vazio)")
        
        # Verificação de inconsistências
        print("\n" + "="*80)
        print("VERIFICAÇÃO DE INCONSISTÊNCIAS")
        print("="*80)
        
        problemas = []
        
        # Verifica se há colunas vazias
        for col in df.columns:
            valores_nao_nulos = df[col].dropna()
            if len(valores_nao_nulos) == 0:
                problemas.append(f"❌ Coluna '{col}' está completamente vazia")
            elif len(valores_nao_nulos) < len(df) * 0.5:
                problemas.append(f"⚠️ Coluna '{col}' tem muitos valores vazios ({len(valores_nao_nulos)}/{len(df)})")
        
        # Verifica se links são válidos
        if 'Link' in df.columns:
            links_invalidos = 0
            for link in df['Link'].dropna():
                if not isinstance(link, str) or not link.startswith('http'):
                    links_invalidos += 1
            
            if links_invalidos > 0:
                problemas.append(f"❌ {links_invalidos} links inválidos encontrados")
        
        # Verifica correspondência entre ID e posição
        if 'ID' in df.columns:
            ids_incorretos = 0
            for i, id_val in enumerate(df['ID']):
                if pd.notna(id_val) and int(id_val) != i + 1:
                    ids_incorretos += 1
            
            if ids_incorretos > 0:
                problemas.append(f"❌ {ids_incorretos} IDs não correspondem à posição na tabela")
        
        if problemas:
            print("🚨 PROBLEMAS ENCONTRADOS:")
            for problema in problemas:
                print(f"   {problema}")
        else:
            print("✅ Nenhum problema encontrado na correspondência dos dados!")
        
        # Gera relatório detalhado
        print("\n" + "="*80)
        print("RELATÓRIO RESUMIDO")
        print("="*80)
        
        print(f"📊 Total de artigos: {len(df)}")
        print(f"📋 Total de colunas: {len(df.columns)}")
        
        if 'Ano' in df.columns:
            anos = df['Ano'].dropna()
            print(f"📅 Período: {anos.min()} - {anos.max()}")
        
        if 'Periódico' in df.columns:
            periodicos_unicos = df['Periódico'].dropna().nunique()
            print(f"📰 Periódicos únicos: {periodicos_unicos}")
        
        if 'ODS (Geral / Específico)' in df.columns:
            ods_info = df['ODS (Geral / Específico)'].dropna()
            print(f"🎯 Artigos com ODS definido: {len(ods_info)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Erro ao verificar arquivo: {e}")
        return None

def gerar_relatorio_html(df):
    """
    Gera um relatório HTML detalhado da verificação
    """
    if df is None:
        return
    
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Verificação - Correspondência de Colunas</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: #ecf0f1; padding: 15px; border-radius: 8px; text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #3498db; }}
        .table-container {{ overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #3498db; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .link-cell {{ max-width: 300px; word-break: break-all; }}
        .status-ok {{ color: #27ae60; font-weight: bold; }}
        .status-warning {{ color: #f39c12; font-weight: bold; }}
        .status-error {{ color: #e74c3c; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Relatório de Verificação - Correspondência de Colunas</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(df)}</div>
                <div>Total de Artigos</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(df.columns)}</div>
                <div>Colunas Disponíveis</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{df['Ano'].min() if 'Ano' in df.columns else 'N/A'}</div>
                <div>Ano Inicial</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{df['Ano'].max() if 'Ano' in df.columns else 'N/A'}</div>
                <div>Ano Final</div>
            </div>
        </div>
        
        <h2>🔍 Verificação das Primeiras 10 Linhas</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
"""
    
    # Adiciona cabeçalhos
    for col in df.columns:
        html_content += f"<th>{col}</th>"
    
    html_content += """
                    </tr>
                </thead>
                <tbody>
"""
    
    # Adiciona primeiras 10 linhas
    for i in range(min(10, len(df))):
        html_content += "<tr>"
        for col in df.columns:
            valor = df.iloc[i][col]
            if pd.notna(valor):
                valor_str = str(valor)
                if len(valor_str) > 100:
                    valor_str = valor_str[:97] + "..."
                
                # Formatação especial para links
                if 'Link' in col and valor_str.startswith('http'):
                    html_content += f'<td class="link-cell"><a href="{valor_str}" target="_blank">{valor_str}</a></td>'
                else:
                    html_content += f"<td>{valor_str}</td>"
            else:
                html_content += "<td><em>(vazio)</em></td>"
        html_content += "</tr>"
    
    html_content += """
                </tbody>
            </table>
        </div>
        
        <h2>📈 Status da Verificação</h2>
        <div style="background: #d5f4e6; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p class="status-ok">✅ Verificação concluída com sucesso!</p>
            <p>Os dados foram carregados e analisados. Verifique os detalhes acima.</p>
        </div>
        
        <p style="text-align: center; color: #7f8c8d; margin-top: 30px;">
            Relatório gerado em """ + pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S') + """
        </p>
    </div>
</body>
</html>
"""
    
    return html_content

def main():
    # Caminho do arquivo Excel
    caminho_excel = r"C:\Users\lucia\Dissertação\Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx"
    
    # Verifica se o arquivo existe
    if not Path(caminho_excel).exists():
        print(f"❌ Erro: Arquivo não encontrado em {caminho_excel}")
        return
    
    # Faz a verificação
    df = verificar_correspondencia_colunas(caminho_excel)
    
    if df is not None:
        # Gera relatório HTML
        html_content = gerar_relatorio_html(df)
        
        # Salva o relatório
        relatorio_path = r"C:\Users\lucia\Dissertação\relatorio_verificacao.html"
        with open(relatorio_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"\n📄 Relatório detalhado salvo em: {relatorio_path}")
        print("🌐 Abra o arquivo HTML no navegador para visualizar o relatório completo!")

if __name__ == "__main__":
    main()
