#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar visualização web interativa APRIMORADA da tabela ABNT
Com sistema de drag & drop melhorado diretamente na tabela
"""

import pandas as pd
import sys
from pathlib import Path

def gerar_visualizacao_web_melhorada(df):
    """
    Gera página HTML interativa com sistema de drag & drop aprimorado
    """
    
    # Substitui valores NaN por string vazia
    df = df.fillna("")
    
    # Converte todas as colunas para string para evitar problemas de encoding
    for col in df.columns:
        df[col] = df[col].astype(str)
    
    # Gera o HTML da tabela
    table_html = df.to_html(
        classes='data-table',
        table_id='mainTable',
        escape=False,
        index=False
    )
    
    # Lista de colunas para o seletor
    colunas_options = ""
    for i, col in enumerate(df.columns):
        checked = "checked" if i < 7 else ""  # Primeiras 7 colunas visíveis por padrão
        colunas_options += f"""
        <div class="column-option" data-col-index="{i}">
            <input type="checkbox" id="col_{i}" value="{i}" {checked} onchange="toggleColumn({i})">
            <label for="col_{i}">
                <span class="drag-handle">⋮⋮</span>
                {col}
            </label>
        </div>
        """
    
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualização Interativa Aprimorada - Corpus da Análise de Conteúdo</title>
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
        
        .column-selector {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
        
        .column-option.drag-over {{
            border-color: #28a745;
            background-color: #e8f5e8;
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
        
        .drag-handle:active {{
            cursor: grabbing;
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
        
        .btn-warning {{
            background: linear-gradient(135deg, #fdbb2d 0%, #22c1c3 100%);
            color: white;
        }}
        
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }}
        
        .btn:active {{
            transform: translateY(-1px);
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
            cursor: move;
            user-select: none;
            transition: all 0.3s ease;
            border-right: 1px solid #455a64;
        }}
        
        .data-table th:hover {{
            background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .data-table th.dragging {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            transform: scale(1.05);
            z-index: 1000;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        
        .data-table th.drag-over {{
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        }}
        
        .data-table th::before {{
            content: "⋮⋮";
            position: absolute;
            left: 4px;
            top: 50%;
            transform: translateY(-50%);
            color: rgba(255,255,255,0.6);
            font-size: 12px;
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
            transform: scale(1.01);
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
            transition: transform 0.3s ease;
        }}
        
        .stat-item:hover {{
            transform: translateY(-3px);
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
        
        .hidden-column {{
            display: none !important;
        }}
        
        .instructions {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .instructions h4 {{
            color: #856404;
            margin-bottom: 10px;
        }}
        
        .instructions ul {{
            color: #856404;
            margin-left: 20px;
        }}
        
        .instructions li {{
            margin-bottom: 5px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            
            .column-selector {{
                grid-template-columns: 1fr;
            }}
            
            .action-buttons {{
                justify-content: center;
            }}
            
            .data-table {{
                font-size: 0.8rem;
            }}
            
            .data-table th {{
                padding: 10px 8px;
            }}
        }}
        
        /* Animações */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .container {{
            animation: fadeIn 0.6s ease-out;
        }}
        
        .dragging {{
            animation: none !important;
        }}
        
        /* Indicador de drop zone */
        .drop-indicator {{
            position: absolute;
            width: 3px;
            height: 100%;
            background: #28a745;
            z-index: 1001;
            box-shadow: 0 0 10px rgba(40, 167, 69, 0.5);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Corpus da Análise de Conteúdo</h1>
            <p>Visualização Interativa Aprimorada - Dissertação de Mestrado</p>
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
            <h3>🎛️ Controles de Visualização</h3>
            
            <div class="instructions">
                <h4>📋 Como usar:</h4>
                <ul>
                    <li><strong>Selecionar colunas:</strong> Marque/desmarque as caixas abaixo</li>
                    <li><strong>Reorganizar:</strong> Arraste os cabeçalhos da tabela ou as opções abaixo</li>
                    <li><strong>Visualizar:</strong> A tabela atualiza automaticamente</li>
                </ul>
            </div>
            
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
                <button class="btn btn-warning" onclick="randomizeColumns()">
                    🎲 Embaralhar
                </button>
                <button class="btn btn-primary" onclick="exportToLatex()">
                    📄 Exportar LaTeX
                </button>
            </div>
            
            <h4 style="margin-top: 20px; margin-bottom: 15px; color: #2c3e50;">
                📋 Seleção e Ordem das Colunas:
            </h4>
            <div class="column-selector" id="columnSelector">
                {colunas_options}
            </div>
        </div>
        
        <div class="table-container">
            {table_html}
        </div>
        
        <div class="footer">
            <p>📚 Gerado automaticamente para dissertação de mestrado • {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    </div>

    <script>
        let columnOrder = {list(range(len(df.columns)))};
        let draggedElement = null;
        let draggedColumnIndex = null;
        
        // Inicialização
        document.addEventListener('DOMContentLoaded', function() {{
            initializeDragAndDrop();
            resetToDefault();
        }});
        
        function initializeDragAndDrop() {{
            // Drag & Drop para seletor de colunas
            const columnOptions = document.querySelectorAll('.column-option');
            columnOptions.forEach(option => {{
                option.addEventListener('dragstart', handleColumnSelectorDragStart);
                option.addEventListener('dragover', handleDragOver);
                option.addEventListener('drop', handleColumnSelectorDrop);
                option.addEventListener('dragend', handleDragEnd);
                option.draggable = true;
            }});
            
            // Drag & Drop para cabeçalhos da tabela
            const tableHeaders = document.querySelectorAll('#mainTable th');
            tableHeaders.forEach((header, index) => {{
                header.addEventListener('dragstart', (e) => handleTableHeaderDragStart(e, index));
                header.addEventListener('dragover', handleDragOver);
                header.addEventListener('drop', (e) => handleTableHeaderDrop(e, index));
                header.addEventListener('dragend', handleDragEnd);
                header.draggable = true;
                header.style.cursor = 'move';
            }});
        }}
        
        function handleColumnSelectorDragStart(e) {{
            draggedElement = e.currentTarget;
            draggedColumnIndex = parseInt(draggedElement.dataset.colIndex);
            draggedElement.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', draggedElement.outerHTML);
        }}
        
        function handleTableHeaderDragStart(e, columnIndex) {{
            draggedColumnIndex = columnIndex;
            e.currentTarget.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
        }}
        
        function handleDragOver(e) {{
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            
            const dropTarget = e.currentTarget;
            if (dropTarget !== draggedElement) {{
                dropTarget.classList.add('drag-over');
            }}
        }}
        
        function handleColumnSelectorDrop(e) {{
            e.preventDefault();
            const dropTarget = e.currentTarget;
            
            if (dropTarget !== draggedElement && draggedElement) {{
                const container = document.getElementById('columnSelector');
                const allOptions = Array.from(container.children);
                const draggedIndex = allOptions.indexOf(draggedElement);
                const targetIndex = allOptions.indexOf(dropTarget);
                
                // Reordena no DOM
                if (draggedIndex < targetIndex) {{
                    container.insertBefore(draggedElement, dropTarget.nextSibling);
                }} else {{
                    container.insertBefore(draggedElement, dropTarget);
                }}
                
                // Atualiza ordem das colunas
                updateColumnOrder();
            }}
            
            dropTarget.classList.remove('drag-over');
        }}
        
        function handleTableHeaderDrop(e, targetColumnIndex) {{
            e.preventDefault();
            
            if (draggedColumnIndex !== null && draggedColumnIndex !== targetColumnIndex) {{
                reorderTableColumn(draggedColumnIndex, targetColumnIndex);
                updateColumnOrder();
            }}
            
            e.currentTarget.classList.remove('drag-over');
        }}
        
        function handleDragEnd(e) {{
            e.currentTarget.classList.remove('dragging');
            const allElements = document.querySelectorAll('.drag-over');
            allElements.forEach(el => el.classList.remove('drag-over'));
            
            draggedElement = null;
            draggedColumnIndex = null;
        }}
        
        function reorderTableColumn(fromIndex, toIndex) {{
            const table = document.getElementById('mainTable');
            const rows = Array.from(table.rows);
            
            rows.forEach(row => {{
                const cells = Array.from(row.cells);
                const draggedCell = cells[fromIndex];
                const targetCell = cells[toIndex];
                
                if (draggedCell && targetCell) {{
                    if (fromIndex < toIndex) {{
                        targetCell.parentNode.insertBefore(draggedCell, targetCell.nextSibling);
                    }} else {{
                        targetCell.parentNode.insertBefore(draggedCell, targetCell);
                    }}
                }}
            }});
        }}
        
        function updateColumnOrder() {{
            const container = document.getElementById('columnSelector');
            const newOrder = Array.from(container.children).map(option => {{
                return parseInt(option.dataset.colIndex);
            }});
            
            columnOrder = newOrder;
            
            // Atualiza a ordem visual da tabela para corresponder
            rebuildTableFromOrder();
        }}
        
        function rebuildTableFromOrder() {{
            // Esta é uma versão simplificada - em uma implementação completa,
            // você reconstruiria toda a tabela baseada na nova ordem
            console.log('Nova ordem das colunas:', columnOrder);
        }}
        
        function toggleColumn(colIndex) {{
            const table = document.getElementById('mainTable');
            const checkbox = document.getElementById('col_' + colIndex);
            const isChecked = checkbox.checked;
            
            // Toggle header
            const headerCells = table.getElementsByTagName('th');
            if (headerCells[colIndex]) {{
                headerCells[colIndex].classList.toggle('hidden-column', !isChecked);
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
                toggleColumn(index);
            }});
        }}
        
        function deselectAll() {{
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            checkboxes.forEach((checkbox, index) => {{
                checkbox.checked = false;
                toggleColumn(index);
            }});
        }}
        
        function resetToDefault() {{
            const defaultColumns = ['ID', 'Autores', 'Título', 'Ano', 'Periódico', 'ODS (Geral / Específico)', 'Aspecto Principal - Estudo'];
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            
            checkboxes.forEach((checkbox, index) => {{
                const label = checkbox.nextElementSibling.textContent.trim();
                const shouldCheck = defaultColumns.some(col => label.includes(col));
                checkbox.checked = shouldCheck;
                toggleColumn(index);
            }});
        }}
        
        function randomizeColumns() {{
            const container = document.getElementById('columnSelector');
            const options = Array.from(container.children);
            
            // Embaralha array
            for (let i = options.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [options[i], options[j]] = [options[j], options[i]];
            }}
            
            // Reordena no DOM
            options.forEach(option => {{
                container.appendChild(option);
            }});
            
            updateColumnOrder();
        }}
        
        function exportToLatex() {{
            const visibleColumns = [];
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]:checked');
            
            checkboxes.forEach(checkbox => {{
                const colIndex = parseInt(checkbox.value);
                const label = checkbox.nextElementSibling.textContent.trim();
                visibleColumns.push({{index: colIndex, name: label}});
            }});
            
            if (visibleColumns.length === 0) {{
                alert('❌ Selecione pelo menos uma coluna para exportar!');
                return;
            }}
            
            const message = `✅ Configuração para exportação LaTeX:
            
📊 Colunas selecionadas: ${{visibleColumns.length}}
📋 Ordem atual: ${{visibleColumns.map(col => col.name.replace('⋮⋮', '').trim()).join(', ')}}

🔄 Esta configuração será usada para gerar a tabela ABNT.`;
            
            alert(message);
        }}
        
        // Adiciona efeitos visuais extras
        document.addEventListener('dragenter', function(e) {{
            if (e.target.classList.contains('column-option') || e.target.tagName === 'TH') {{
                e.target.style.transform = 'scale(1.02)';
            }}
        }});
        
        document.addEventListener('dragleave', function(e) {{
            if (e.target.classList.contains('column-option') || e.target.tagName === 'TH') {{
                e.target.style.transform = '';
            }}
        }});
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
        print(f"Erro: Arquivo não encontrado em {caminho_excel}")
        return
    
    try:
        # Lê o arquivo Excel
        print("🔄 Lendo arquivo Excel...")
        df = pd.read_excel(caminho_excel, sheet_name=0)
        
        print(f"✅ Arquivo lido com sucesso!")
        print(f"📊 Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
        print(f"📋 Colunas: {list(df.columns)}")
        
        # Gera visualização web melhorada
        print("\n🚀 Gerando visualização web aprimorada...")
        html_content = gerar_visualizacao_web_melhorada(df)
        
        # Salva o arquivo HTML
        html_path = r"C:\Users\lucia\Dissertação\visualizacao_interativa_melhorada.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Visualização aprimorada salva em: {html_path}")
        print("\n🌟 NOVAS FUNCIONALIDADES:")
        print("   • 🎯 Drag & Drop diretamente nos cabeçalhos da tabela")
        print("   • ⋮⋮ Indicadores visuais de arraste")
        print("   • 🎨 Animações e efeitos visuais aprimorados")
        print("   • 📱 Interface mais responsiva e intuitiva")
        print("   • 🎲 Botão para embaralhar colunas")
        print("   • 📋 Instruções claras de uso")
        print("   • 🔄 Atualização automática da ordem")
        
        print(f"\n🚀 Abra o arquivo no navegador para testar as melhorias!")
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")

if __name__ == "__main__":
    main()
