#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para melhorar a visualização:
1. Remover debug logs
2. Adicionar mensagem quando não há dados selecionados
3. Implementar reordenação de colunas por drag & drop
"""

import pandas as pd
import os
import json

def criar_visualizacao_melhorada():
    """Cria versão melhorada da visualização"""
    
    # Carregar dados
    try:
        df = pd.read_excel('Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx')
        print(f"✅ Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
    except Exception as e:
        print(f"❌ Erro ao carregar Excel: {e}")
        return
    
    # Mapeamento dos ícones ODS
    ods_icons = {
        '1': 'SDG-icon-PT--01-2-01.png',
        '2': 'SDG-icon-PT--02-2.png', 
        '3': 'SDG-icon-PT--03-2.png',
        '4': 'SDG-icon-PT--04-2-01.png',
        '5': 'SDG-icon-PT--05-2.png',
        '6': 'SDG-icon-PT--06-2-01.png',
        '7': 'SDG-icon-PT--07-2-01.png',
        '8': 'SDG-icon-PT--08-2-01.png',
        '9': 'SDG-icon-PT--09-2.png',
        '10': 'SDG-icon-PT--10-2.png',
        '11': 'SDG-icon-PT--11-2.png',
        '12': 'SDG-icon-PT--12-2-01.png',
        '13': 'SDG-icon-PT--13-2.png',
        '14': 'SDG-icon-PT--14-2-01.png',
        '15': 'SDG-icon-PT--15-2-01.png',
        '16': 'SDG-icon-PT--16-2.png',
        '17': 'SDG-icon-PT--17-2.png'
    }
    
    # Encontrar coluna ODS
    ods_column = None
    for col in df.columns:
        if 'ODS' in str(col).upper():
            ods_column = col
            break
    
    print(f"🎯 Coluna ODS identificada: {ods_column}")
    
    # HTML template melhorado
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualização Interativa - Análise de Conteúdo</title>
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
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
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
            padding: 25px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .btn {{
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
        }}
        
        .btn:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .btn-danger {{
            background-color: #dc3545;
        }}
        
        .btn-danger:hover {{
            background-color: #c82333;
        }}
        
        .btn-success {{
            background-color: #28a745;
        }}
        
        .btn-success:hover {{
            background-color: #218838;
        }}
        
        .btn-warning {{
            background-color: #ffc107;
            color: #212529;
        }}
        
        .btn-warning:hover {{
            background-color: #e0a800;
        }}
        
        .column-selector {{
            margin: 20px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            border: 1px solid #ddd;
        }}
        
        .column-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .column-item {{
            display: flex;
            align-items: center;
            padding: 12px;
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            cursor: move;
            transition: all 0.2s;
            user-select: none;
        }}
        
        .column-item:hover {{
            background: #e9ecef;
            border-color: #007bff;
        }}
        
        .column-item.dragging {{
            opacity: 0.5;
            transform: scale(0.95);
        }}
        
        .column-item.drag-over {{
            border-color: #28a745;
            background: #d4edda;
        }}
        
        .column-item input {{
            margin-right: 12px;
            transform: scale(1.2);
        }}
        
        .column-name {{
            font-weight: 500;
            color: #333;
            flex: 1;
        }}
        
        .drag-handle {{
            margin-left: 10px;
            color: #6c757d;
            cursor: grab;
        }}
        
        .drag-handle:active {{
            cursor: grabbing;
        }}
        
        .table-container {{
            margin: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
            background: #f8f9fa;
            border-radius: 8px;
            margin: 20px;
        }}
        
        .empty-state-icon {{
            font-size: 4rem;
            margin-bottom: 20px;
            opacity: 0.5;
        }}
        
        .empty-state h3 {{
            margin-bottom: 10px;
            color: #495057;
        }}
        
        .empty-state p {{
            margin-bottom: 20px;
        }}
        
        #mainTable {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            background: white;
        }}
        
        #mainTable th {{
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
            padding: 15px 10px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #0056b3;
            position: sticky;
            top: 0;
            z-index: 100;
            cursor: move;
            user-select: none;
        }}
        
        #mainTable th:hover {{
            background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
        }}
        
        #mainTable th.dragging {{
            opacity: 0.5;
        }}
        
        #mainTable td {{
            padding: 12px 10px;
            border: 1px solid #dee2e6;
            background-color: white;
            vertical-align: top;
        }}
        
        #mainTable tr:nth-child(even) td {{
            background-color: #f8f9fa;
        }}
        
        #mainTable tr:hover td {{
            background-color: #e3f2fd;
        }}
        
        .hidden-column {{
            display: none !important;
        }}
        
        .ods-icon {{
            width: 32px;
            height: 32px;
            margin: 2px;
            border-radius: 4px;
            display: inline-block;
            transition: transform 0.2s;
        }}
        
        .ods-icon:hover {{
            transform: scale(1.1);
        }}
        
        .ods-geral {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .status-bar {{
            padding: 15px 30px;
            background: #e9ecef;
            border-top: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            color: #495057;
        }}
        
        .status-info {{
            display: flex;
            gap: 20px;
        }}
        
        @media (max-width: 768px) {{
            .column-grid {{
                grid-template-columns: 1fr;
            }}
            
            .status-bar {{
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }}
            
            .status-info {{
                flex-direction: column;
                gap: 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Visualização Interativa</h1>
            <p>Análise de Conteúdo com Corpus Corrigido - Dissertação de Mestrado</p>
        </div>
        
        <div class="controls">
            <h3>🎛️ Controles de Visualização</h3>
            <div style="margin-top: 15px;">
                <button class="btn btn-success" onclick="selectAllColumns()">✅ Selecionar Todas</button>
                <button class="btn btn-danger" onclick="deselectAllColumns()">❌ Desmarcar Todas</button>
                <button class="btn" onclick="resetToDefaultColumns()">🔄 Configuração Padrão</button>
                <button class="btn btn-warning" onclick="showOnlyODSColumns()">🎯 Apenas ODS</button>
            </div>
        </div>
        
        <div class="column-selector">
            <h4>📋 Seleção e Ordenação de Colunas</h4>
            <p style="color: #6c757d; margin-bottom: 15px;">
                Marque/desmarque colunas e arraste para reordenar. Os cabeçalhos da tabela também podem ser arrastados.
            </p>
            <div class="column-grid" id="columnGrid">
                <!-- Colunas serão inseridas aqui dinamicamente -->
            </div>
        </div>
        
        <div id="tableContainer">
            <!-- Tabela ou estado vazio será inserido aqui -->
        </div>
        
        <div class="status-bar">
            <div class="status-info">
                <span id="totalRecords">Total: {len(df)} registros</span>
                <span id="visibleColumns">Colunas visíveis: 0</span>
                <span id="totalColumns">Total de colunas: {len(df.columns)}</span>
            </div>
            <div>
                <span>Desenvolvido para Dissertação de Mestrado</span>
            </div>
        </div>
    </div>

    <script>
        // DADOS GLOBAIS
        const data = {json.dumps(df.to_dict('records'), ensure_ascii=False, indent=2)};
        const columns = {json.dumps(list(df.columns), ensure_ascii=False)};
        const odsIcons = {json.dumps(ods_icons, ensure_ascii=False)};
        const odsColumn = '{ods_column}';
        
        let columnOrder = [...columns];
        let selectedColumns = [];
        
        // INICIALIZAÇÃO
        document.addEventListener('DOMContentLoaded', function() {{
            initializeApp();
        }});
        
        function initializeApp() {{
            // Configuração padrão
            const defaultColumns = ['ID', 'Autores', 'Título', 'Ano', 'Periódico', 'ODS (Geral / Específico)', 'Aspecto Principal - Estudo'];
            selectedColumns = columns.filter(col => defaultColumns.includes(col));
            
            createColumnSelector();
            renderTable();
            updateStatus();
        }}
        
        function createColumnSelector() {{
            const grid = document.getElementById('columnGrid');
            grid.innerHTML = '';
            
            columnOrder.forEach((columnName, index) => {{
                const isSelected = selectedColumns.includes(columnName);
                
                const item = document.createElement('div');
                item.className = 'column-item';
                item.draggable = true;
                item.dataset.columnName = columnName;
                item.dataset.originalIndex = index;
                
                item.innerHTML = `
                    <input type="checkbox" id="col_${{index}}" ${{isSelected ? 'checked' : ''}} onchange="toggleColumnSelection('${{columnName}}')">
                    <label for="col_${{index}}" class="column-name">${{columnName}}</label>
                    <span class="drag-handle">⋮⋮</span>
                `;
                
                // Drag events
                item.addEventListener('dragstart', handleDragStart);
                item.addEventListener('dragover', handleDragOver);
                item.addEventListener('drop', handleDrop);
                item.addEventListener('dragend', handleDragEnd);
                
                grid.appendChild(item);
            }});
        }}
        
        function toggleColumnSelection(columnName) {{
            if (selectedColumns.includes(columnName)) {{
                selectedColumns = selectedColumns.filter(col => col !== columnName);
            }} else {{
                selectedColumns.push(columnName);
            }}
            
            renderTable();
            updateStatus();
        }}
        
        function selectAllColumns() {{
            selectedColumns = [...columns];
            updateColumnCheckboxes();
            renderTable();
            updateStatus();
        }}
        
        function deselectAllColumns() {{
            selectedColumns = [];
            updateColumnCheckboxes();
            renderTable();
            updateStatus();
        }}
        
        function resetToDefaultColumns() {{
            const defaultColumns = ['ID', 'Autores', 'Título', 'Ano', 'Periódico', 'ODS (Geral / Específico)', 'Aspecto Principal - Estudo'];
            selectedColumns = columns.filter(col => defaultColumns.includes(col));
            updateColumnCheckboxes();
            renderTable();
            updateStatus();
        }}
        
        function showOnlyODSColumns() {{
            selectedColumns = columns.filter(col => 
                col.includes('ID') || 
                col.includes('Título') || 
                col.includes('ODS')
            );
            updateColumnCheckboxes();
            renderTable();
            updateStatus();
        }}
        
        function updateColumnCheckboxes() {{
            columnOrder.forEach((columnName, index) => {{
                const checkbox = document.getElementById(`col_${{index}}`);
                if (checkbox) {{
                    checkbox.checked = selectedColumns.includes(columnName);
                }}
            }});
        }}
        
        function renderTable() {{
            const container = document.getElementById('tableContainer');
            
            if (selectedColumns.length === 0) {{
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📊</div>
                        <h3>Nenhuma coluna selecionada</h3>
                        <p>Selecione uma ou mais colunas para visualizar os dados.</p>
                        <button class="btn" onclick="resetToDefaultColumns()">🔄 Usar Configuração Padrão</button>
                    </div>
                `;
                return;
            }}
            
            // Ordenar colunas selecionadas conforme a ordem definida
            const orderedSelectedColumns = columnOrder.filter(col => selectedColumns.includes(col));
            
            let tableHTML = `
                <div class="table-container">
                    <table id="mainTable">
                        <thead>
                            <tr>
            `;
            
            orderedSelectedColumns.forEach(columnName => {{
                tableHTML += `<th draggable="true" data-column="${{columnName}}">${{columnName}}</th>`;
            }});
            
            tableHTML += `
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.forEach(row => {{
                tableHTML += '<tr>';
                orderedSelectedColumns.forEach(columnName => {{
                    let cellValue = row[columnName] || '';
                    
                    if (columnName === odsColumn && cellValue) {{
                        cellValue = formatODSCell(cellValue);
                    }} else {{
                        cellValue = String(cellValue).substring(0, 200); // Limitar texto longo
                        if (cellValue.length > 150) cellValue += '...';
                    }}
                    
                    tableHTML += `<td>${{cellValue}}</td>`;
                }});
                tableHTML += '</tr>';
            }});
            
            tableHTML += `
                        </tbody>
                    </table>
                </div>
            `;
            
            container.innerHTML = tableHTML;
            
            // Adicionar drag & drop aos cabeçalhos
            addHeaderDragAndDrop();
        }}
        
        function formatODSCell(value) {{
            if (!value) return '';
            
            const valueStr = String(value).trim();
            
            // Caso especial para "Geral" - usar logo circular dos ODS
            if (valueStr.toLowerCase().includes('geral')) {{
                return `<div class="ods-geral">
                    <img src="logo-sepado.png" alt="ODS Geral" class="ods-icon" title="Objetivos de Desenvolvimento Sustentável" style="width: 40px; height: 40px; border-radius: 50%;">
                    <span style="font-size: 11px; font-weight: bold;">GERAL</span>
                </div>`;
            }}
            
            // Buscar números de ODS no texto
            const odsNumbers = valueStr.match(/\\b(\\d{{1,2}})\\b/g) || [];
            const validODS = odsNumbers.filter(num => odsIcons[num]);
            
            if (validODS.length > 0) {{
                const icons = validODS.map(num => 
                    `<img src="Ícones oficiais - ODS/${{odsIcons[num]}}" alt="ODS ${{num}}" class="ods-icon" title="ODS ${{num}}">`
                ).join('');
                return `<div style="display: flex; align-items: center; gap: 5px;">${{icons}} <span style="font-size: 11px;">${{valueStr}}</span></div>`;
            }}
            
            return valueStr;
        }}
        
        function updateStatus() {{
            document.getElementById('visibleColumns').textContent = `Colunas visíveis: ${{selectedColumns.length}}`;
        }}
        
        // DRAG & DROP para colunas
        let draggedElement = null;
        
        function handleDragStart(e) {{
            draggedElement = this;
            this.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', this.outerHTML);
        }}
        
        function handleDragOver(e) {{
            if (e.preventDefault) {{
                e.preventDefault();
            }}
            
            this.classList.add('drag-over');
            e.dataTransfer.dropEffect = 'move';
            return false;
        }}
        
        function handleDrop(e) {{
            if (e.stopPropagation) {{
                e.stopPropagation();
            }}
            
            if (draggedElement !== this) {{
                const draggedColumn = draggedElement.dataset.columnName;
                const targetColumn = this.dataset.columnName;
                
                // Reordenar array
                const draggedIndex = columnOrder.indexOf(draggedColumn);
                const targetIndex = columnOrder.indexOf(targetColumn);
                
                columnOrder.splice(draggedIndex, 1);
                columnOrder.splice(targetIndex, 0, draggedColumn);
                
                // Recriar interface
                createColumnSelector();
                renderTable();
            }}
            
            return false;
        }}
        
        function handleDragEnd(e) {{
            const items = document.querySelectorAll('.column-item');
            items.forEach(item => {{
                item.classList.remove('dragging', 'drag-over');
            }});
            draggedElement = null;
        }}
        
        // DRAG & DROP para cabeçalhos da tabela
        function addHeaderDragAndDrop() {{
            const headers = document.querySelectorAll('#mainTable th');
            headers.forEach(header => {{
                header.addEventListener('dragstart', function(e) {{
                    e.dataTransfer.setData('text/plain', this.dataset.column);
                    this.classList.add('dragging');
                }});
                
                header.addEventListener('dragover', function(e) {{
                    e.preventDefault();
                }});
                
                header.addEventListener('drop', function(e) {{
                    e.preventDefault();
                    const draggedColumn = e.dataTransfer.getData('text/plain');
                    const targetColumn = this.dataset.column;
                    
                    if (draggedColumn !== targetColumn) {{
                        // Reordenar colunas
                        const draggedIndex = columnOrder.indexOf(draggedColumn);
                        const targetIndex = columnOrder.indexOf(targetColumn);
                        
                        columnOrder.splice(draggedIndex, 1);
                        columnOrder.splice(targetIndex, 0, draggedColumn);
                        
                        // Atualizar interface
                        createColumnSelector();
                        renderTable();
                    }}
                }});
                
                header.addEventListener('dragend', function() {{
                    this.classList.remove('dragging');
                }});
            }});
        }}
    </script>
</body>
</html>"""
    
    # Salvar arquivo
    output_file = 'visualizacao_MELHORADA_FINAL.html'
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Arquivo salvo: {output_file}")
        print(f"🌐 Abra em: file:///{os.path.abspath(output_file)}")
        
        # Verificar se o arquivo foi criado
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"📁 Tamanho do arquivo: {size:,} bytes")
        
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")

if __name__ == "__main__":
    print("🚀 Criando visualização MELHORADA FINAL...")
    criar_visualizacao_melhorada()
    print("✅ Processo concluído!")
