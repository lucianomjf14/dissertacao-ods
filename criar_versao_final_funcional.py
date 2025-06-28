#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar versão FINAL FUNCIONAL da visualização interativa
com foco na função "Desmarcar Todas" funcionando perfeitamente
"""

import pandas as pd
import os
import json
from pathlib import Path

def criar_visualizacao_final():
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
    
    # HTML template com JavaScript SUPER SIMPLES e FUNCIONAL
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualização Final - Dissertação</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #007bff;
        }}
        
        .controls {{
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }}
        
        .btn {{
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            margin: 5px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }}
        
        .btn:hover {{
            background-color: #0056b3;
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
        
        .column-selector {{
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: white;
            margin-bottom: 20px;
        }}
        
        .checkbox-container {{
            display: flex;
            align-items: center;
            margin: 5px 0;
            padding: 5px;
            border-radius: 3px;
        }}
        
        .checkbox-container:hover {{
            background-color: #f0f0f0;
        }}
        
        .checkbox-container input {{
            margin-right: 10px;
        }}
        
        .col-name {{
            font-weight: 500;
            color: #333;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin-top: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        
        #mainTable {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }}
        
        #mainTable th {{
            background-color: #007bff;
            color: white;
            padding: 10px 8px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #0056b3;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        #mainTable td {{
            padding: 8px;
            border: 1px solid #ddd;
            background-color: white;
        }}
        
        #mainTable tr:nth-child(even) td {{
            background-color: #f8f9fa;
        }}
        
        .hidden-column {{
            display: none !important;
        }}
        
        .ods-icon {{
            width: 30px;
            height: 30px;
            margin: 2px;
            border-radius: 3px;
            display: inline-block;
        }}
        
        .ods-geral {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 2px;
        }}
        
        .status {{
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            font-weight: bold;
        }}
        
        .status-info {{
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }}
        
        .debug-info {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f1f3f4;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Visualização Final - Análise de Conteúdo</h1>
            <p>Versão com foco na função "Desmarcar Todas" funcionando perfeitamente</p>
        </div>
        
        <div class="controls">
            <h3>Controles de Colunas</h3>
            <div>
                <button class="btn btn-success" onclick="selectAllColumns()">✅ Marcar Todas</button>
                <button class="btn btn-danger" onclick="deselectAllColumns()">❌ DESMARCAR TODAS</button>
                <button class="btn" onclick="resetToDefaultColumns()">🔄 Padrão</button>
                <button class="btn" onclick="showOnlyODSColumns()">🎯 Apenas ODS</button>
            </div>
            
            <div class="status status-info" id="statusMessage">
                Pronto para uso. Use os botões acima para controlar as colunas.
            </div>
        </div>
        
        <div class="column-selector" id="columnSelector">
            <h4>Selecionar Colunas:</h4>
            <div id="checkboxContainer"></div>
        </div>
        
        <div class="table-container">
            <table id="mainTable">
                <thead id="tableHeader"></thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>
        
        <div class="debug-info" id="debugInfo">
            <strong>Debug Info:</strong><br>
            <div id="debugLog"></div>
        </div>
    </div>

    <script>
        // VARIÁVEIS GLOBAIS
        let tableData = [];
        let columnNames = [];
        let defaultColumns = ['ID', 'Autores', 'Título', 'Ano', 'Periódico', 'ODS (Geral / Específico)', 'Aspecto Principal - Estudo'];
        
        // DADOS DA TABELA
        const data = {json.dumps(df.to_dict('records'), ensure_ascii=False, indent=2)};
        const columns = {json.dumps(list(df.columns), ensure_ascii=False)};
        
        // MAPEAMENTO DE ÍCONES ODS
        const odsIcons = {json.dumps(ods_icons, ensure_ascii=False)};
        
        // LOG FUNCTION
        function logDebug(message) {{
            console.log(message);
            const debugLog = document.getElementById('debugLog');
            if (debugLog) {{
                debugLog.innerHTML += message + '<br>';
                debugLog.scrollTop = debugLog.scrollHeight;
            }}
        }}
        
        // STATUS MESSAGE
        function updateStatus(message, type = 'info') {{
            const statusEl = document.getElementById('statusMessage');
            if (statusEl) {{
                statusEl.textContent = message;
                statusEl.className = `status status-${{type}}`;
            }}
            logDebug(`📱 Status: ${{message}}`);
        }}
        
        // INICIALIZAÇÃO
        function initializeApp() {{
            logDebug('🚀 Inicializando aplicação...');
            
            tableData = data;
            columnNames = columns;
            
            logDebug(`📊 Dados carregados: ${{tableData.length}} linhas, ${{columnNames.length}} colunas`);
            
            createColumnCheckboxes();
            renderTable();
            
            updateStatus(`Aplicação carregada: ${{tableData.length}} registros, ${{columnNames.length}} colunas`);
            logDebug('✅ Inicialização concluída');
        }}
        
        // CRIAR CHECKBOXES DAS COLUNAS
        function createColumnCheckboxes() {{
            logDebug('📋 Criando checkboxes das colunas...');
            
            const container = document.getElementById('checkboxContainer');
            if (!container) {{
                logDebug('❌ Container de checkboxes não encontrado');
                return;
            }}
            
            container.innerHTML = '';
            
            columnNames.forEach((columnName, index) => {{
                const isDefault = defaultColumns.includes(columnName);
                
                const checkboxDiv = document.createElement('div');
                checkboxDiv.className = 'checkbox-container';
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `col_${{index}}`;
                checkbox.value = index;
                checkbox.checked = isDefault;
                checkbox.onchange = function() {{ toggleColumn(index); }};
                
                const label = document.createElement('label');
                label.htmlFor = `col_${{index}}`;
                label.innerHTML = `<span class="col-name">${{columnName}}</span>`;
                
                checkboxDiv.appendChild(checkbox);
                checkboxDiv.appendChild(label);
                container.appendChild(checkboxDiv);
            }});
            
            logDebug(`✅ ${{columnNames.length}} checkboxes criados`);
        }}
        
        // TOGGLE COLUMN VISIBILITY
        function toggleColumn(columnIndex) {{
            const checkbox = document.getElementById(`col_${{columnIndex}}`);
            if (!checkbox) {{
                logDebug(`❌ Checkbox para coluna ${{columnIndex}} não encontrado`);
                return;
            }}
            
            const isVisible = checkbox.checked;
            const thElements = document.querySelectorAll(`#mainTable th:nth-child(${{columnIndex + 1}})`);
            const tdElements = document.querySelectorAll(`#mainTable td:nth-child(${{columnIndex + 1}})`);
            
            // Aplicar/remover classe hidden
            [...thElements, ...tdElements].forEach(element => {{
                if (isVisible) {{
                    element.classList.remove('hidden-column');
                }} else {{
                    element.classList.add('hidden-column');
                }}
            }});
            
            logDebug(`🔄 Coluna ${{columnIndex}} (${{columnNames[columnIndex]}}) ${{isVisible ? 'mostrada' : 'ocultada'}}`);
        }}
        
        // FUNÇÃO PRINCÍPAL: DESMARCAR TODAS AS COLUNAS
        function deselectAllColumns() {{
            logDebug('🔥 INICIANDO: Desmarcar TODAS as colunas');
            updateStatus('Desmarcando todas as colunas...', 'info');
            
            const checkboxes = document.querySelectorAll('#checkboxContainer input[type="checkbox"]');
            logDebug(`📋 Encontrados ${{checkboxes.length}} checkboxes`);
            
            if (checkboxes.length === 0) {{
                logDebug('❌ ERRO: Nenhum checkbox encontrado!');
                updateStatus('ERRO: Nenhum checkbox encontrado!', 'error');
                return;
            }}
            
            let processedCount = 0;
            
            // Processar cada checkbox
            checkboxes.forEach((checkbox, index) => {{
                const columnIndex = parseInt(checkbox.value);
                logDebug(`☐ Processando checkbox ${{index}}: coluna ${{columnIndex}} (${{columnNames[columnIndex]}})`);
                
                // Desmarcar checkbox
                checkbox.checked = false;
                
                // Ocultar coluna
                const thElements = document.querySelectorAll(`#mainTable th:nth-child(${{columnIndex + 1}})`);
                const tdElements = document.querySelectorAll(`#mainTable td:nth-child(${{columnIndex + 1}})`);
                
                [...thElements, ...tdElements].forEach(element => {{
                    element.classList.add('hidden-column');
                }});
                
                processedCount++;
            }});
            
            logDebug(`✅ CONCLUÍDO: ${{processedCount}} colunas desmarcadas e ocultadas`);
            updateStatus(`SUCESSO: ${{processedCount}} colunas desmarcadas`, 'success');
            
            // Verificação final
            setTimeout(() => {{
                const visibleColumns = document.querySelectorAll('#mainTable th:not(.hidden-column)').length;
                const hiddenColumns = document.querySelectorAll('#mainTable th.hidden-column').length;
                logDebug(`🔍 Verificação final: ${{visibleColumns}} visíveis, ${{hiddenColumns}} ocultas`);
                
                if (hiddenColumns === columnNames.length) {{
                    updateStatus('✅ PERFEITO: Todas as colunas foram desmarcadas!', 'success');
                }} else {{
                    updateStatus(`⚠️ ATENÇÃO: ${{visibleColumns}} colunas ainda visíveis`, 'warning');
                }}
            }}, 100);
        }}
        
        // MARCAR TODAS AS COLUNAS
        function selectAllColumns() {{
            logDebug('✅ INICIANDO: Marcar todas as colunas');
            updateStatus('Marcando todas as colunas...', 'info');
            
            const checkboxes = document.querySelectorAll('#checkboxContainer input[type="checkbox"]');
            let processedCount = 0;
            
            checkboxes.forEach((checkbox, index) => {{
                const columnIndex = parseInt(checkbox.value);
                checkbox.checked = true;
                
                const thElements = document.querySelectorAll(`#mainTable th:nth-child(${{columnIndex + 1}})`);
                const tdElements = document.querySelectorAll(`#mainTable td:nth-child(${{columnIndex + 1}})`);
                
                [...thElements, ...tdElements].forEach(element => {{
                    element.classList.remove('hidden-column');
                }});
                
                processedCount++;
            }});
            
            logDebug(`✅ ${{processedCount}} colunas marcadas`);
            updateStatus(`${{processedCount}} colunas selecionadas`, 'success');
        }}
        
        // RESETAR PARA PADRÃO
        function resetToDefaultColumns() {{
            logDebug('🔄 INICIANDO: Reset para colunas padrão');
            updateStatus('Resetando para configuração padrão...', 'info');
            
            const checkboxes = document.querySelectorAll('#checkboxContainer input[type="checkbox"]');
            let selectedCount = 0;
            
            checkboxes.forEach((checkbox, index) => {{
                const columnIndex = parseInt(checkbox.value);
                const columnName = columnNames[columnIndex];
                const shouldBeVisible = defaultColumns.includes(columnName);
                
                checkbox.checked = shouldBeVisible;
                
                const thElements = document.querySelectorAll(`#mainTable th:nth-child(${{columnIndex + 1}})`);
                const tdElements = document.querySelectorAll(`#mainTable td:nth-child(${{columnIndex + 1}})`);
                
                [...thElements, ...tdElements].forEach(element => {{
                    if (shouldBeVisible) {{
                        element.classList.remove('hidden-column');
                        selectedCount++;
                    }} else {{
                        element.classList.add('hidden-column');
                    }}
                }});
            }});
            
            logDebug(`✅ Reset concluído: ${{selectedCount}} colunas padrão`);
            updateStatus(`Configuração padrão: ${{selectedCount}} colunas`, 'success');
        }}
        
        // MOSTRAR APENAS COLUNAS ODS
        function showOnlyODSColumns() {{
            logDebug('🎯 INICIANDO: Mostrar apenas colunas ODS');
            
            const odsRelatedColumns = ['ID', 'Título', 'ODS (Geral / Específico)'];
            const checkboxes = document.querySelectorAll('#checkboxContainer input[type="checkbox"]');
            let selectedCount = 0;
            
            checkboxes.forEach((checkbox, index) => {{
                const columnIndex = parseInt(checkbox.value);
                const columnName = columnNames[columnIndex];
                const shouldBeVisible = odsRelatedColumns.some(odsCol => columnName.includes(odsCol));
                
                checkbox.checked = shouldBeVisible;
                
                const thElements = document.querySelectorAll(`#mainTable th:nth-child(${{columnIndex + 1}})`);
                const tdElements = document.querySelectorAll(`#mainTable td:nth-child(${{columnIndex + 1}})`);
                
                [...thElements, ...tdElements].forEach(element => {{
                    if (shouldBeVisible) {{
                        element.classList.remove('hidden-column');
                        selectedCount++;
                    }} else {{
                        element.classList.add('hidden-column');
                    }}
                }});
            }});
            
            logDebug(`✅ Apenas ODS: ${{selectedCount}} colunas`);
            updateStatus(`Modo ODS: ${{selectedCount}} colunas`, 'success');
        }}
        
        // RENDERIZAR TABELA
        function renderTable() {{
            logDebug('🎨 Renderizando tabela...');
            
            const headerContainer = document.getElementById('tableHeader');
            const bodyContainer = document.getElementById('tableBody');
            
            if (!headerContainer || !bodyContainer) {{
                logDebug('❌ Containers da tabela não encontrados');
                return;
            }}
            
            // Cabeçalho
            const headerRow = document.createElement('tr');
            columnNames.forEach((columnName, index) => {{
                const th = document.createElement('th');
                th.textContent = columnName;
                if (!defaultColumns.includes(columnName)) {{
                    th.classList.add('hidden-column');
                }}
                headerRow.appendChild(th);
            }});
            headerContainer.innerHTML = '';
            headerContainer.appendChild(headerRow);
            
            // Corpo da tabela
            bodyContainer.innerHTML = '';
            tableData.forEach((row, rowIndex) => {{
                const tr = document.createElement('tr');
                
                columnNames.forEach((columnName, columnIndex) => {{
                    const td = document.createElement('td');
                    let cellValue = row[columnName] || '';
                    
                    // Processamento especial para coluna ODS
                    if (columnName === '{ods_column}' && cellValue) {{
                        td.innerHTML = formatODSCell(cellValue);
                    }} else {{
                        td.textContent = cellValue;
                    }}
                    
                    if (!defaultColumns.includes(columnName)) {{
                        td.classList.add('hidden-column');
                    }}
                    
                    tr.appendChild(td);
                }});
                
                bodyContainer.appendChild(tr);
            }});
            
            logDebug(`✅ Tabela renderizada: ${{tableData.length}} linhas`);
        }}
        
        // FORMATAR CÉLULA ODS COM ÍCONES
        function formatODSCell(value) {{
            if (!value) return '';
            
            const valueStr = String(value).trim();
            
            // Caso especial para "Geral"
            if (valueStr.toLowerCase().includes('geral')) {{
                return `<div class="ods-geral">
                    <img src="Ícones oficiais - ODS/SDG-icon-PT--01-2-01.png" alt="ODS 1" class="ods-icon" title="ODS 1">
                    <img src="Ícones oficiais - ODS/SDG-icon-PT--03-2.png" alt="ODS 3" class="ods-icon" title="ODS 3">
                    <img src="Ícones oficiais - ODS/SDG-icon-PT--04-2-01.png" alt="ODS 4" class="ods-icon" title="ODS 4">
                    <img src="Ícones oficiais - ODS/SDG-icon-PT--08-2-01.png" alt="ODS 8" class="ods-icon" title="ODS 8">
                    <img src="Ícones oficiais - ODS/SDG-icon-PT--11-2.png" alt="ODS 11" class="ods-icon" title="ODS 11">
                    <span style="font-size: 10px; margin-left: 5px;">Geral</span>
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
        
        // INICIALIZAR QUANDO A PÁGINA CARREGAR
        document.addEventListener('DOMContentLoaded', function() {{
            logDebug('📖 Página carregada, inicializando...');
            initializeApp();
        }});
        
        // LOG DE FUNÇÕES DISPONÍVEIS
        window.addEventListener('load', function() {{
            logDebug('🔧 Funções disponíveis:');
            logDebug(`  - selectAllColumns: ${{typeof selectAllColumns}}`);
            logDebug(`  - deselectAllColumns: ${{typeof deselectAllColumns}}`);
            logDebug(`  - resetToDefaultColumns: ${{typeof resetToDefaultColumns}}`);
            logDebug(`  - showOnlyODSColumns: ${{typeof showOnlyODSColumns}}`);
        }});
        
    </script>
</body>
</html>"""
    
    # Salvar arquivo
    output_file = 'visualizacao_FINAL_FUNCIONAL.html'
    
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
    print("🚀 Criando visualização FINAL FUNCIONAL...")
    criar_visualizacao_final()
    print("✅ Processo concluído!")
