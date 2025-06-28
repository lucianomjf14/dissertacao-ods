#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para diagnosticar e corrigir problema de correspondência de colunas
"""

import pandas as pd
from pathlib import Path

def diagnosticar_problema_colunas(caminho_arquivo):
    """
    Diagnostica problema de correspondência entre seleção e visualização
    """
    try:
        # Lê o arquivo Excel
        print("🔍 Diagnosticando problema de correspondência de colunas...")
        df = pd.read_excel(caminho_arquivo, sheet_name=0)
        
        print(f"📊 Dados carregados: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        # Lista as colunas com seus índices
        print("\n📋 MAPEAMENTO ATUAL DAS COLUNAS:")
        print("="*80)
        for i, col in enumerate(df.columns):
            print(f"Índice {i:2d}: '{col}'")
        
        # Verifica se há problemas de encoding ou caracteres especiais
        print("\n🔍 VERIFICAÇÃO DE PROBLEMAS:")
        print("="*80)
        
        problemas = []
        
        for i, col in enumerate(df.columns):
            # Verifica caracteres especiais
            if any(char in col for char in ['/', '(', ')', '-', ' ']):
                problemas.append(f"Coluna {i} '{col}' contém caracteres especiais")
            
            # Verifica se nome é muito longo
            if len(col) > 30:
                problemas.append(f"Coluna {i} '{col}' tem nome muito longo ({len(col)} chars)")
        
        if problemas:
            print("⚠️ Problemas encontrados:")
            for problema in problemas:
                print(f"   {problema}")
        else:
            print("✅ Nenhum problema óbvio encontrado com nomes das colunas")
        
        return df
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def gerar_visualizacao_corrigida(df):
    """
    Gera visualização com mapeamento correto de colunas
    """
    
    # Substitui valores NaN por string vazia
    df = df.fillna("")
    
    # Converte todas as colunas para string
    for col in df.columns:
        df[col] = df[col].astype(str)
    
    # Cria mapeamento limpo das colunas
    colunas_mapeamento = {}
    for i, col in enumerate(df.columns):
        # Limpa o nome da coluna para uso em JavaScript
        col_limpo = col.replace('(', '').replace(')', '').replace('/', '_').replace(' ', '_')
        colunas_mapeamento[i] = {
            'original': col,
            'limpo': col_limpo,
            'index': i
        }
    
    # Gera o HTML da tabela
    table_html = df.to_html(
        classes='data-table',
        table_id='mainTable',
        escape=False,
        index=False
    )
    
    # Lista de colunas para o seletor com índices corretos
    colunas_options = ""
    for i, col in enumerate(df.columns):
        checked = "checked" if i < 7 else ""  # Primeiras 7 colunas visíveis por padrão
        col_id = f"col_{i}"
        col_display = col[:50] + "..." if len(col) > 50 else col
        
        colunas_options += f"""
        <div class="column-option" data-col-index="{i}">
            <input type="checkbox" id="{col_id}" value="{i}" {checked} onchange="toggleColumn({i})">
            <label for="{col_id}">
                <span class="drag-handle">⋮⋮</span>
                <span class="col-index">[{i}]</span>
                <span class="col-name">{col_display}</span>
            </label>
        </div>
        """
    
    # JavaScript corrigido
    js_colunas_array = str(list(range(len(df.columns))))
    
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualização CORRIGIDA - Corpus da Análise de Conteúdo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 100%;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .controls {{
            background: #f8f9fa;
            padding: 25px;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .controls h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }}
        
        .debug-info {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .debug-info h4 {{
            color: #856404;
            margin-bottom: 10px;
        }}
        
        .debug-info p {{
            color: #856404;
            font-size: 0.9rem;
            margin-bottom: 5px;
        }}
        
        .column-selector {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .column-option {{
            display: flex;
            align-items: center;
            background: white;
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
            cursor: move;
            user-select: none;
        }}
        
        .column-option:hover {{
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .column-option.dragging {{
            opacity: 0.6;
            transform: rotate(3deg) scale(1.05);
            z-index: 1000;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        
        .column-option input[type="checkbox"] {{
            margin-right: 10px;
            transform: scale(1.3);
            cursor: pointer;
        }}
        
        .column-option label {{
            cursor: move;
            flex: 1;
            font-weight: 500;
            color: #2c3e50;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .drag-handle {{
            color: #6c757d;
            font-size: 16px;
            font-weight: bold;
            cursor: grab;
        }}
        
        .col-index {{
            background: #007bff;
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            min-width: 30px;
            text-align: center;
        }}
        
        .col-name {{
            flex: 1;
        }}
        
        .action-buttons {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}
        
        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .btn-secondary {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}
        
        .btn-success {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }}
        
        .btn-debug {{
            background: linear-gradient(135deg, #fdbb2d 0%, #22c1c3 100%);
            color: white;
        }}
        
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }}
        
        .table-container {{
            padding: 20px;
            overflow-x: auto;
            max-height: 70vh;
            overflow-y: auto;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9rem;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .data-table th {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            font-weight: 600;
            padding: 15px 12px;
            text-align: left;
            position: sticky;
            top: 0;
            z-index: 100;
            border-right: 1px solid #455a64;
            position: relative;
        }}
        
        .data-table th::before {{
            content: attr(data-col-index);
            position: absolute;
            top: 2px;
            right: 2px;
            background: #e74c3c;
            color: white;
            padding: 1px 4px;
            border-radius: 3px;
            font-size: 0.7rem;
            font-weight: bold;
        }}
        
        .data-table td {{
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
            border-right: 1px solid #dee2e6;
            vertical-align: top;
            word-wrap: break-word;
            max-width: 300px;
            transition: all 0.3s ease;
        }}
        
        .data-table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        .data-table tr:hover {{
            background-color: #e3f2fd;
        }}
        
        .hidden-column {{
            display: none !important;
        }}
        
        .stats {{
            background: #e8f4f8;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }}
        
        .stats h4 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .stat-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            display: block;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #6c757d;
            margin-top: 5px;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9rem;
        }}
        
        @media (max-width: 768px) {{
            .column-selector {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Visualização CORRIGIDA - Debug Mode</h1>
            <p>Diagnóstico e Correção do Problema de Correspondência de Colunas</p>
        </div>
        
        <div class="stats">
            <h4>📈 Estatísticas do Corpus</h4>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-number">{len(df)}</span>
                    <div class="stat-label">Total de Artigos</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(df.columns)}</span>
                    <div class="stat-label">Colunas Disponíveis</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{df['Ano'].min() if 'Ano' in df.columns else 'N/A'}</span>
                    <div class="stat-label">Ano Inicial</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{df['Ano'].max() if 'Ano' in df.columns else 'N/A'}</span>
                    <div class="stat-label">Ano Final</div>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <div class="debug-info">
                <h4>🐛 Modo Debug Ativo</h4>
                <p>• Os números em vermelho nos cabeçalhos mostram o índice real da coluna</p>
                <p>• Os números em azul nos seletores mostram o índice que será usado</p>
                <p>• Use o botão "Debug Info" para ver informações detalhadas</p>
                <p>• Se uma coluna aparecer errada, verifique se os índices coincidem</p>
            </div>
            
            <h3>🎛️ Controles de Visualização</h3>
            
            <div class="action-buttons">
                <button class="btn btn-primary" onclick="selectAll()">
                    ✅ Selecionar Todas
                </button>
                <button class="btn btn-secondary" onclick="deselectAll()">
                    ❌ Desmarcar Todas
                </button>
                <button class="btn btn-success" onclick="resetToDefault()">
                    🔄 Padrão ABNT
                </button>
                <button class="btn btn-debug" onclick="showDebugInfo()">
                    🐛 Debug Info
                </button>
            </div>
            
            <h4 style="margin-top: 20px; margin-bottom: 15px; color: #2c3e50;">
                📋 Seleção de Colunas (com índices para debug):
            </h4>
            <div class="column-selector" id="columnSelector">
                {colunas_options}
            </div>
        </div>
        
        <div class="table-container">
            {table_html}
        </div>
        
        <div class="footer">
            <p>🔧 Modo Debug • Gerado em {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    </div>

    <script>
        // Array com os nomes das colunas para debug
        const columnNames = {[f'"{col}"' for col in df.columns]};
        const totalColumns = {len(df.columns)};
        
        // Adiciona índices aos cabeçalhos da tabela para debug
        document.addEventListener('DOMContentLoaded', function() {{
            const headers = document.querySelectorAll('#mainTable th');
            headers.forEach((header, index) => {{
                header.setAttribute('data-col-index', index);
                header.title = `Coluna ${{index}}: ${{columnNames[index]}}`;
            }});
            
            // Aplica configuração padrão
            resetToDefault();
        }});
        
        function toggleColumn(colIndex) {{
            console.log(`Toggling column ${{colIndex}}: ${{columnNames[colIndex]}}`);
            
            const table = document.getElementById('mainTable');
            const checkbox = document.getElementById('col_' + colIndex);
            const isChecked = checkbox.checked;
            
            // Toggle header
            const headerCells = table.getElementsByTagName('th');
            if (headerCells[colIndex]) {{
                headerCells[colIndex].classList.toggle('hidden-column', !isChecked);
                console.log(`Header ${{colIndex}} (${{headerCells[colIndex].textContent}}) ${{isChecked ? 'shown' : 'hidden'}}`);
            }}
            
            // Toggle data cells
            const rows = table.getElementsByTagName('tr');
            for (let i = 1; i < rows.length; i++) {{
                const cells = rows[i].getElementsByTagName('td');
                if (cells[colIndex]) {{
                    cells[colIndex].classList.toggle('hidden-column', !isChecked);
                }}
            }}
        }}
        
        function selectAll() {{
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            checkboxes.forEach((checkbox, index) => {{
                checkbox.checked = true;
                toggleColumn(parseInt(checkbox.value));
            }});
        }}
        
        function deselectAll() {{
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            checkboxes.forEach((checkbox, index) => {{
                checkbox.checked = false;
                toggleColumn(parseInt(checkbox.value));
            }});
        }}
        
        function resetToDefault() {{
            // Colunas padrão ABNT: ID, Autores, Título, Ano, Periódico, ODS, Aspecto Principal
            const defaultIndexes = [1, 2, 3, 4, 5, 13, 14]; // Índices das colunas padrão
            
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            checkboxes.forEach((checkbox, index) => {{
                const colIndex = parseInt(checkbox.value);
                const shouldCheck = defaultIndexes.includes(colIndex);
                checkbox.checked = shouldCheck;
                toggleColumn(colIndex);
            }});
            
            console.log('Configuração padrão aplicada:', defaultIndexes);
        }}
        
        function showDebugInfo() {{
            let info = 'INFORMAÇÕES DE DEBUG:\\n\\n';
            info += `Total de colunas: ${{totalColumns}}\\n\\n`;
            
            info += 'MAPEAMENTO DAS COLUNAS:\\n';
            columnNames.forEach((name, index) => {{
                info += `${{index}}: ${{name}}\\n`;
            }});
            
            info += '\\nCOLUNAS ATUALMENTE VISÍVEIS:\\n';
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]:checked');
            checkboxes.forEach(checkbox => {{
                const colIndex = parseInt(checkbox.value);
                info += `${{colIndex}}: ${{columnNames[colIndex]}}\\n`;
            }});
            
            alert(info);
        }}
    </script>
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
    
    # Diagnostica o problema
    df = diagnosticar_problema_colunas(caminho_excel)
    
    if df is not None:
        print("\n🔧 Gerando visualização corrigida com modo debug...")
        html_content = gerar_visualizacao_corrigida(df)
        
        # Salva o arquivo HTML corrigido
        html_path = r"C:\Users\lucia\Dissertação\visualizacao_debug.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Visualização debug salva em: {html_path}")
        print("\n🐛 FUNCIONALIDADES DE DEBUG:")
        print("   • 🔴 Números vermelhos nos cabeçalhos = índice real da coluna")
        print("   • 🔵 Números azuis nos seletores = índice que será usado")
        print("   • 🐛 Botão 'Debug Info' = mostra mapeamento completo")
        print("   • 📋 Console do navegador = logs detalhados das ações")
        print("\n🚀 Abra o arquivo e teste o problema específico!")

if __name__ == "__main__":
    main()
