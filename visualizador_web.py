#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar visualização web da tabela ABNT
Gera uma página HTML interativa para visualizar os dados
"""

import pandas as pd
import sys
from pathlib import Path
import webbrowser

def ler_excel_e_gerar_tabela_abnt(caminho_arquivo):
    """
    Lê arquivo Excel e retorna DataFrame
    """
    try:
        # Lê o arquivo Excel
        print(f"Lendo arquivo: {caminho_arquivo}")
        
        # Tenta ler todas as planilhas
        xl_file = pd.ExcelFile(caminho_arquivo)
        print(f"Planilhas encontradas: {xl_file.sheet_names}")
        
        # Lê a primeira planilha
        df = pd.read_excel(caminho_arquivo, sheet_name=0)
        
        print(f"Dimensões dos dados: {df.shape[0]} linhas x {df.shape[1]} colunas")
        print(f"Colunas: {list(df.columns)}")
        
        return df, xl_file.sheet_names
        
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None, None

def gerar_html_visualizacao(df):
    """
    Gera página HTML com visualização interativa dos dados
    """
    
    # CSS para estilização
    css_style = """
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        h2 {
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
        }
        
        .info-box {
            background-color: #e8f4fd;
            border: 1px solid #3498db;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin: 20px 0;
        }
        
        .stat-item {
            background-color: #3498db;
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            min-width: 150px;
            margin: 5px;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px 8px;
            text-align: left;
            vertical-align: top;
        }
        
        th {
            background-color: #3498db;
            color: white;
            font-weight: bold;
            position: sticky;
            top: 0;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        tr:hover {
            background-color: #e3f2fd;
        }
        
        .title-cell {
            max-width: 400px;
            word-wrap: break-word;
        }
        
        .author-cell {
            max-width: 200px;
            word-wrap: break-word;
        }
        
        .journal-cell {
            max-width: 250px;
            word-wrap: break-word;
        }
        
        .search-box {
            margin: 20px 0;
            padding: 10px;
            width: 100%;
            max-width: 400px;
            border: 2px solid #3498db;
            border-radius: 5px;
            font-size: 16px;
        }
        
        .filter-buttons {
            margin: 10px 0;
        }
        
        .filter-btn {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 15px;
            margin: 2px;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .filter-btn:hover {
            background-color: #2980b9;
        }
        
        .filter-btn.active {
            background-color: #e74c3c;
        }
        
        .table-container {
            overflow-x: auto;
            margin: 20px 0;
        }
        
        .export-buttons {
            margin: 20px 0;
            text-align: center;
        }
        
        .export-btn {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        
        .export-btn:hover {
            background-color: #229954;
        }
    </style>
    """
    
    # JavaScript para funcionalidades interativas
    javascript = """
    <script>
        function searchTable() {
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const table = document.getElementById('dataTable');
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                const cells = row.getElementsByTagName('td');
                let found = false;
                
                for (let j = 0; j < cells.length; j++) {
                    if (cells[j].textContent.toLowerCase().includes(filter)) {
                        found = true;
                        break;
                    }
                }
                
                row.style.display = found ? '' : 'none';
            }
        }
        
        function filterByYear(year) {
            const table = document.getElementById('dataTable');
            const rows = table.getElementsByTagName('tr');
            
            // Remove active class from all buttons
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            event.target.classList.add('active');
            
            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                const yearCell = row.getElementsByTagName('td')[3]; // Coluna do ano
                
                if (year === 'all' || yearCell.textContent.includes(year)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            }
        }
        
        function exportToCSV() {
            const table = document.getElementById('dataTable');
            const rows = table.getElementsByTagName('tr');
            let csv = '';
            
            for (let i = 0; i < rows.length; i++) {
                const row = rows[i];
                if (row.style.display !== 'none') {
                    const cells = row.getElementsByTagName(i === 0 ? 'th' : 'td');
                    const rowData = [];
                    
                    for (let j = 0; j < cells.length; j++) {
                        let cellData = cells[j].textContent.replace(/"/g, '""');
                        rowData.push('"' + cellData + '"');
                    }
                    
                    csv += rowData.join(',') + '\\n';
                }
            }
            
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'corpus_analise_conteudo.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        }
        
        function printTable() {
            window.print();
        }
    </script>
    """
    
    # Processa dados para estatísticas
    total_artigos = len(df)
    anos_unicos = sorted(df['Ano'].unique()) if 'Ano' in df.columns else []
    periodicos_unicos = df['Periódico'].nunique() if 'Periódico' in df.columns else 0
    
    # Contagem por ano
    contagem_anos = df['Ano'].value_counts().sort_index() if 'Ano' in df.columns else {}
    
    # Início do HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Corpus da Análise de Conteúdo - Visualização Interativa</title>
        {css_style}
    </head>
    <body>
        <div class="container">
            <h1>📊 Corpus da Análise de Conteúdo</h1>
            <h2>Artigos Selecionados para Dissertação de Mestrado</h2>
            
            <div class="info-box">
                <strong>ℹ️ Sobre esta visualização:</strong><br>
                Esta página apresenta o corpus completo da análise de conteúdo, 
                permitindo visualização interativa, busca e filtragem dos artigos selecionados.
            </div>
            
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">{total_artigos}</span>
                    <span>Total de Artigos</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(anos_unicos)}</span>
                    <span>Anos Cobertos</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{periodicos_unicos}</span>
                    <span>Periódicos Únicos</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{min(anos_unicos) if anos_unicos else 'N/A'}-{max(anos_unicos) if anos_unicos else 'N/A'}</span>
                    <span>Período de Publicação</span>
                </div>
            </div>
            
            <h2>🔍 Busca e Filtros</h2>
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 Buscar por autor, título, periódico..." onkeyup="searchTable()">
            
            <div class="filter-buttons">
                <strong>Filtrar por ano:</strong><br>
                <button class="filter-btn active" onclick="filterByYear('all')">Todos</button>
    """
    
    # Adiciona botões de filtro por ano
    for ano in sorted(anos_unicos, reverse=True):
        contagem = contagem_anos.get(ano, 0)
        html_content += f'<button class="filter-btn" onclick="filterByYear(\'{ano}\')">{ano} ({contagem})</button>'
    
    html_content += """
            </div>
            
            <div class="export-buttons">
                <button class="export-btn" onclick="exportToCSV()">📥 Exportar CSV</button>
                <button class="export-btn" onclick="printTable()">🖨️ Imprimir</button>
            </div>
            
            <h2>📋 Tabela de Dados</h2>
            <div class="table-container">
                <table id="dataTable">
                    <thead>
                        <tr>
    """
    
    # Colunas principais para exibição
    colunas_exibir = ['ID', 'Autores', 'Título', 'Ano', 'Periódico']
    if 'ODS (Geral / Específico)' in df.columns:
        colunas_exibir.append('ODS (Geral / Específico)')
    
    # Cabeçalho da tabela
    for col in colunas_exibir:
        if col in df.columns:
            html_content += f"<th>{col}</th>"
    
    html_content += """
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # Linhas de dados
    for _, row in df.iterrows():
        html_content += "<tr>"
        for col in colunas_exibir:
            if col in df.columns:
                valor = str(row[col]) if pd.notna(row[col]) else ""
                
                # Aplica classes CSS específicas
                css_class = ""
                if col == 'Título':
                    css_class = 'title-cell'
                elif col == 'Autores':
                    css_class = 'author-cell'
                elif col == 'Periódico':
                    css_class = 'journal-cell'
                
                html_content += f'<td class="{css_class}">{valor}</td>'
        html_content += "</tr>"
    
    # Finaliza HTML
    html_content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="info-box">
                <strong>📈 Distribuição por Ano:</strong><br>
    """
    
    # Adiciona estatísticas por ano
    for ano, count in contagem_anos.items():
        percentage = (count / total_artigos) * 100
        html_content += f"{ano}: {count} artigos ({percentage:.1f}%) | "
    
    html_content += f"""
            </div>
            
            <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
                <p><strong>Fonte:</strong> Elaborado pelo autor, 2025</p>
                <p>Gerado automaticamente em {pd.Timestamp.now().strftime('%d/%m/%Y às %H:%M')}</p>
            </div>
        </div>
        
        {javascript}
    </body>
    </html>
    """
    
    return html_content

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
        print("GERANDO VISUALIZAÇÃO WEB")
        print("="*80)
        
        # Gera o HTML
        html_content = gerar_html_visualizacao(df)
        
        # Salva o arquivo HTML
        caminho_html = r"C:\Users\lucia\Dissertação\visualizacao_corpus.html"
        with open(caminho_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Arquivo HTML gerado: {caminho_html}")
        
        # Abre no navegador
        print("🌐 Abrindo no navegador...")
        webbrowser.open(f"file:///{caminho_html}")
        
        print("\n" + "="*80)
        print("FUNCIONALIDADES DA PÁGINA WEB:")
        print("="*80)
        print("🔍 Busca em tempo real por qualquer termo")
        print("📅 Filtros por ano de publicação")
        print("📊 Estatísticas visuais dos dados")
        print("📥 Exportação para CSV")
        print("🖨️ Impressão da tabela")
        print("📱 Design responsivo para dispositivos móveis")
        print("✨ Tabela interativa com destaque ao passar o mouse")
        
    else:
        print("Não foi possível processar o arquivo Excel.")

if __name__ == "__main__":
    main()
