#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar visualização com ícones ODS
"""

import pandas as pd
from pathlib import Path
import re

def mapear_ods_para_icones(valor_ods):
    """
    Mapeia os valores ODS para os ícones correspondentes
    """
    if pd.isna(valor_ods) or valor_ods == "":
        return ""
    
    # Caso especial para "Geral" - cria ícone composto
    if str(valor_ods).strip() == "Geral":
        icones_principais = [1, 3, 7, 11, 13, 16]  # ODS mais relacionados a cidades sustentáveis
        icones_html = []
        for num in icones_principais:
            if num == 1:
                icone = "SDG-icon-PT--01-2-01.png"
            elif num == 3:
                icone = "SDG-icon-PT--03-2.png"
            elif num == 7:
                icone = "SDG-icon-PT--07-2-01.png"
            elif num == 11:
                icone = "SDG-icon-PT--11-2.png"
            elif num == 13:
                icone = "SDG-icon-PT--13-2.png"
            elif num == 16:
                icone = "SDG-icon-PT--16-2.png"
            
            caminho_icone = f"Ícones oficiais - ODS/{icone}"
            icones_html.append(f'<img src="{caminho_icone}" alt="ODS {num}" title="ODS {num} (Geral)" class="ods-icon ods-icon-geral">')
        
        return '<div class="ods-geral-container" title="ODS Geral - Múltiplos Objetivos">' + " ".join(icones_html) + '<span class="ods-geral-label">GERAL</span></div>'
    
    # Extrai números ODS usando regex
    numeros_ods = re.findall(r'ODS (\d+)', str(valor_ods))
    
    icones_html = []
    for num in numeros_ods:
        # Mapeia o número para o arquivo de ícone correspondente
        if num == "1":
            icone = "SDG-icon-PT--01-2-01.png"
        elif num == "2":
            icone = "SDG-icon-PT--02-2.png"
        elif num == "3":
            icone = "SDG-icon-PT--03-2.png"
        elif num == "4":
            icone = "SDG-icon-PT--04-2-01.png"
        elif num == "5":
            icone = "SDG-icon-PT--05-2.png"
        elif num == "6":
            icone = "SDG-icon-PT--06-2-01.png"
        elif num == "7":
            icone = "SDG-icon-PT--07-2-01.png"
        elif num == "8":
            icone = "SDG-icon-PT--08-2-01.png"
        elif num == "9":
            icone = "SDG-icon-PT--09-2.png"
        elif num == "10":
            icone = "SDG-icon-PT--10-2.png"
        elif num == "11":
            icone = "SDG-icon-PT--11-2.png"
        elif num == "12":
            icone = "SDG-icon-PT--12-2-01.png"
        elif num == "13":
            icone = "SDG-icon-PT--13-2.png"
        elif num == "14":
            icone = "SDG-icon-PT--14-2-01.png"
        elif num == "15":
            icone = "SDG-icon-PT--15-2-01.png"
        elif num == "16":
            icone = "SDG-icon-PT--16-2.png"
        elif num == "17":
            icone = "SDG-icon-PT--17-2.png"
        else:
            continue
          # Caminho relativo para o ícone
        caminho_icone = f"Ícones oficiais - ODS/{icone}"
        icones_html.append(f'<img src="{caminho_icone}" alt="ODS {num}" title="ODS {num}" class="ods-icon">')
    
    if icones_html:
        if len(icones_html) > 1:
            return f'<div class="ods-multi-container" title="{valor_ods}">' + " ".join(icones_html) + '</div>'
        else:
            return icones_html[0]
    else:
        return valor_ods

def gerar_visualizacao_com_icones_ods():
    """
    Gera visualização com ícones ODS
    """
    try:
        # Carrega os dados
        print("🎨 Criando visualização com ícones ODS...")
        df = pd.read_excel("Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx", sheet_name=0)
        
        print(f"📊 Dados carregados: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        # Substitui valores NaN
        df = df.fillna("")
        
        # Converte todas as colunas para string
        for col in df.columns:
            df[col] = df[col].astype(str)
        
        # Encontra o índice da coluna ODS
        coluna_ods_index = None
        for i, col in enumerate(df.columns):
            if "ODS" in col and "Geral" in col:
                coluna_ods_index = i
                break
        
        print(f"🎯 Coluna ODS encontrada no índice: {coluna_ods_index}")
        
        # Cria uma cópia do DataFrame para modificar
        df_display = df.copy()
        
        # Aplica ícones na coluna ODS
        if coluna_ods_index is not None:
            coluna_ods_nome = df.columns[coluna_ods_index]
            df_display[coluna_ods_nome] = df[coluna_ods_nome].apply(mapear_ods_para_icones)
        
        # Cria mapeamento das colunas
        colunas_info = []
        for i, col in enumerate(df.columns):
            colunas_info.append({
                'index': i,
                'name': col,
                'id': f'col_{i}',
                'display_name': col[:50] + "..." if len(col) > 50 else col,
                'is_ods': i == coluna_ods_index
            })
        
        # Gera tabela HTML
        table_html = df_display.to_html(
            classes='data-table',
            table_id='mainTable',
            escape=False,
            index=False
        )
        
        # Cria checkboxes
        colunas_checkboxes = ""
        for info in colunas_info:
            checked = "checked" if info['index'] < 7 else ""
            icone_ods = "🎯" if info['is_ods'] else ""
            
            colunas_checkboxes += f"""
        <div class="column-option" data-col-index="{info['index']}" data-original-index="{info['index']}">
            <input type="checkbox" id="{info['id']}" value="{info['index']}" {checked} onchange="toggleColumn({info['index']})">
            <label for="{info['id']}">
                <span class="drag-handle">⋮⋮</span>
                <span class="col-index">[{info['index']}]</span>
                <span class="col-name">{icone_ods} {info['display_name']}</span>
            </label>
        </div>
        """
        
        # Array JavaScript com informações das colunas
        js_colunas_info = str([{
            'index': info['index'],
            'name': info['name'],
            'id': info['id'],
            'is_ods': info['is_ods']
        } for info in colunas_info])
        
        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Visualização com Ícones ODS - Corpus da Análise de Conteúdo</title>
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
        
        .ods-notice {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 20px;
            margin: 0;
            text-align: center;
            font-weight: bold;
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
        
        .action-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center;
        }}
        
        .btn {{
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .btn-success {{
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
        }}
        
        .btn-warning {{
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
        }}
        
        .btn-secondary {{
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
            color: white;
        }}
        
        .btn-ods {{
            background: linear-gradient(135degrees, #e74c3c 0%, #c0392b 100%);
            color: white;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        
        .ods-instructions {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .ods-instructions h4 {{
            color: #856404;
            margin-bottom: 10px;
        }}
        
        .ods-instructions p {{
            color: #856404;
            font-size: 0.9rem;
            margin-bottom: 5px;
        }}
        
        .column-selector {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }}
        
        .column-option {{
            display: flex;
            align-items: center;
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .column-option:hover {{
            border-color: #e74c3c;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .column-option input[type="checkbox"] {{
            margin-right: 12px;
            transform: scale(1.3);
            cursor: pointer;
        }}
        
        .column-option label {{
            display: flex;
            align-items: center;
            cursor: pointer;
            width: 100%;
            font-size: 0.9rem;
        }}
        
        .drag-handle {{
            color: #6c757d;
            margin-right: 10px;
            font-size: 16px;
        }}
        
        .col-index {{
            background: #007bff;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-right: 10px;
            min-width: 35px;
            text-align: center;
        }}
        
        .col-name {{
            font-weight: 500;
            color: #2c3e50;
        }}
        
        .table-container {{
            max-height: 80vh;
            overflow: auto;
            margin: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            background: white;
        }}
        
        .data-table th {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 100;
            border-right: 1px solid #455a64;
        }}
        
        .data-table td {{
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
            border-right: 1px solid #dee2e6;
            vertical-align: top;
            word-wrap: break-word;
            max-width: 300px;
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
          /* Estilos específicos para ícones ODS */
        .ods-icon {{
            width: 45px;
            height: 45px;
            margin: 3px;
            border-radius: 6px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
            vertical-align: middle;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .ods-icon:hover {{
            transform: scale(1.15);
            box-shadow: 0 6px 15px rgba(0,0,0,0.25);
            border-color: #3498db;
        }}
        
        /* Estilos para ODS Geral */
        .ods-geral-container {{
            display: inline-flex;
            align-items: center;
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            padding: 8px 12px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            margin: 2px;
            position: relative;
            transition: all 0.3s ease;
        }}
        
        .ods-geral-container:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(243, 156, 18, 0.3);
        }}
        
        .ods-icon-geral {{
            width: 25px;
            height: 25px;
            margin: 1px;
            opacity: 0.9;
        }}
        
        .ods-icon-geral:hover {{
            transform: scale(1.1);
            opacity: 1;
        }}
        
        .ods-geral-label {{
            font-size: 0.7rem;
            font-weight: bold;
            color: white;
            margin-left: 6px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        }}
        
        /* Container para múltiplos ODS */
        .ods-multi-container {{
            display: inline-flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 2px;
        }}
        
        .stats {{
            background: #e8f4f8;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            border-left: 5px solid #e74c3c;
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
            color: #e74c3c;
            display: block;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #6c757d;
            margin-top: 5px;
        }}
        
        .instructions {{
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .instructions h4 {{
            color: #0c5460;
            margin-bottom: 10px;
        }}
        
        .instructions ul {{
            color: #0c5460;
            margin-left: 20px;
        }}
        
        .instructions li {{
            margin-bottom: 5px;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9rem;
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
            
            .ods-icon {{
                width: 35px;
                height: 35px;
            }}
            
            .ods-icon-geral {{
                width: 20px;
                height: 20px;
            }}
            
            .ods-geral-label {{
                font-size: 0.6rem;
            }}
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .container {{
            animation: fadeIn 0.6s ease-out;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Corpus da Análise de Conteúdo</h1>
            <p>Visualização com Ícones Oficiais dos ODS</p>
        </div>
        
        <div class="ods-notice">
            🎨 NOVA FUNCIONALIDADE: A coluna ODS agora exibe os ícones oficiais dos Objetivos de Desenvolvimento Sustentável!
        </div>
        
        <div class="stats">
            <h4>📈 Estatísticas do Corpus</h4>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-number">{df.shape[0]}</span>
                    <div class="stat-label">Total de Artigos</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{df.shape[1]}</span>
                    <div class="stat-label">Colunas Disponíveis</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">2020</span>
                    <div class="stat-label">Ano Inicial</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">2024</span>
                    <div class="stat-label">Ano Final</div>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <h3>🎛️ Controles de Visualização</h3>
              <div class="instructions">
                <h4>📋 Como usar (COM ÍCONES ODS APRIMORADOS):</h4>
                <ul>
                    <li><strong>🎯 Ícones ODS:</strong> Ícones maiores (45x45px) para melhor visualização</li>
                    <li><strong>🌟 Ícone Geral:</strong> Artigos "Geral" mostram ícone especial com múltiplos ODS</li>
                    <li><strong>Múltiplos ODS:</strong> Artigos com vários ODS mostram todos os ícones organizados</li>
                    <li><strong>Efeitos melhorados:</strong> Hover com escala, sombra e borda azul</li>
                    <li><strong>Mobile responsivo:</strong> Ícones se ajustam automaticamente</li>
                </ul>
            </div>
              <div class="ods-instructions">
                <h4>🎨 Sobre os Ícones ODS Aprimorados</h4>
                <p><strong>Tamanho:</strong> 45x45px (35x35px no mobile) para melhor visibilidade</p>
                <p><strong>Ícone Geral:</strong> Fundo dourado com ODS principais (1,3,7,11,13,16) + label "GERAL"</p>
                <p><strong>Múltiplos ODS:</strong> Container organizado para artigos com vários objetivos</p>
                <p><strong>Efeitos:</strong> Hover com escala 115%, sombra e borda azul</p>
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
                </button>                <button class="btn btn-ods" onclick="mostrarApenasODS()">
                    🎯 Mostrar Apenas ODS
                </button>
                <button class="btn btn-warning" onclick="testODSIcons()">
                    🧪 Testar Ícones ODS
                </button>
                <button class="btn btn-success" onclick="demonstrarIconeGeral()">
                    🌟 Demo Ícone Geral
                </button>
                <button class="btn btn-primary" onclick="exportToLatex()">
                    📄 Exportar LaTeX
                </button>
            </div>
            
            <h4 style="margin-top: 20px; margin-bottom: 15px; color: #2c3e50;">
                📋 Seleção de Colunas (🎯 = Coluna com Ícones ODS):
            </h4>
            <div class="column-selector" id="columnSelector">
                {colunas_checkboxes}
            </div>
        </div>
        
        <div class="table-container">
            {table_html}
        </div>
        
        <div class="footer">
            <p>🎯 Visualização com Ícones ODS | Dissertação de Mestrado | Ícones Oficiais das Nações Unidas</p>
        </div>
    </div>

    <script>
        // Informações das colunas carregadas do Python
        const columnsInfo = {js_colunas_info};
        
        console.log('🎯 Sistema com ícones ODS inicializado');
        console.log('📊 Total de colunas mapeadas:', columnsInfo.length);
        
        // Encontra a coluna ODS
        const odsColumnIndex = columnsInfo.find(col => col.is_ods)?.index;
        console.log('🎯 Coluna ODS identificada no índice:', odsColumnIndex);
        
        // Função para alternar visibilidade das colunas
        function toggleColumn(colIndex) {{
            console.log(`🔧 Alternando coluna índice: ${{colIndex}}`);
            
            const table = document.getElementById('mainTable');
            const checkbox = document.getElementById('col_' + colIndex);
            
            if (!checkbox) {{
                console.error(`❌ Checkbox não encontrado: col_${{colIndex}}`);
                return;
            }}
            
            const isChecked = checkbox.checked;
            const isODSColumn = colIndex === odsColumnIndex;
            
            console.log(`📊 Coluna ${{colIndex}} está ${{isChecked ? 'marcada' : 'desmarcada'}}${{isODSColumn ? ' (COLUNA ODS COM ÍCONES!)' : ''}}`);
            
            // Alterna header
            const headerCells = table.getElementsByTagName('th');
            if (headerCells[colIndex]) {{
                headerCells[colIndex].classList.toggle('hidden-column', !isChecked);
            }}
            
            // Alterna células de dados
            const rows = table.getElementsByTagName('tr');
            for (let i = 1; i < rows.length; i++) {{
                const cells = rows[i].getElementsByTagName('td');
                if (cells[colIndex]) {{
                    cells[colIndex].classList.toggle('hidden-column', !isChecked);
                }}
            }}
            
            if (isODSColumn && isChecked) {{
                console.log('🎯 Coluna ODS ativada - ícones devem estar visíveis!');
            }}
        }}
        
        function selectAll() {{
            console.log('🔄 Selecionando todas as colunas...');
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            checkboxes.forEach((checkbox) => {{
                const colIndex = parseInt(checkbox.value);
                checkbox.checked = true;
                toggleColumn(colIndex);
            }});
        }}
        
        function deselectAll() {{
            console.log('🔄 Desmarcando todas as colunas...');
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            checkboxes.forEach((checkbox) => {{
                const colIndex = parseInt(checkbox.value);
                checkbox.checked = false;
                toggleColumn(colIndex);
            }});
        }}
        
        function resetToDefault() {{
            console.log('🔄 Resetando para configuração padrão...');
            const defaultColumns = ['ID', 'Autores', 'Título', 'Ano', 'Periódico', 'ODS (Geral / Específico)', 'Aspecto Principal - Estudo'];
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            
            checkboxes.forEach((checkbox) => {{
                const colIndex = parseInt(checkbox.value);
                const label = checkbox.parentElement.querySelector('.col-name').textContent.trim();
                const shouldCheck = defaultColumns.some(col => label.includes(col));
                checkbox.checked = shouldCheck;
                toggleColumn(colIndex);
            }});
        }}
        
        function mostrarApenasODS() {{
            console.log('🎯 Mostrando apenas colunas essenciais + ODS...');
            const essentialColumns = ['ID', 'Autores', 'Título', 'Ano', 'ODS (Geral / Específico)'];
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            
            checkboxes.forEach((checkbox) => {{
                const colIndex = parseInt(checkbox.value);
                const label = checkbox.parentElement.querySelector('.col-name').textContent.trim();
                const shouldCheck = essentialColumns.some(col => label.includes(col));
                checkbox.checked = shouldCheck;
                toggleColumn(colIndex);
            }});
            
            alert('🎯 Visualização focada em ODS ativada!\\n\\nApenas as colunas essenciais + ODS estão visíveis para destacar os ícones dos Objetivos de Desenvolvimento Sustentável.');
        }}
        
        function demonstrarIconeGeral() {{
            console.log('🌟 Demonstrando ícone Geral...');
            
            // Primeiro desmarca todas
            deselectAll();
            
            setTimeout(() => {{
                // Ativa apenas ID, Título e ODS
                const essentialColumns = [1, 3, odsColumnIndex]; // ID, Título, ODS
                
                essentialColumns.forEach(index => {{
                    if (index !== undefined) {{
                        const checkbox = document.getElementById('col_' + index);
                        if (checkbox) {{
                            checkbox.checked = true;
                            toggleColumn(index);
                        }}
                    }}
                }});
                
                setTimeout(() => {{
                    // Destaca elementos "Geral" na tabela
                    const geralElements = document.querySelectorAll('.ods-geral-container');
                    geralElements.forEach((element, i) => {{
                        setTimeout(() => {{
                            element.style.transform = 'scale(1.2)';
                            element.style.boxShadow = '0 8px 25px rgba(243, 156, 18, 0.6)';
                            element.style.border = '3px solid #3498db';
                            
                            setTimeout(() => {{
                                element.style.transform = '';
                                element.style.boxShadow = '';
                                element.style.border = '';
                            }}, 2000);
                        }}, i * 500);
                    }});
                    
                    const geralCount = geralElements.length;
                    alert(`🌟 Demonstração do Ícone "Geral" Completa!
                    
🎨 Características do ícone Geral:
• Fundo laranja/dourado distintivo
• Contém os principais ODS relacionados a cidades sustentáveis
• Inclui ODS 1, 3, 7, 11, 13, 16
• Label "GERAL" para identificação clara
• Efeito hover diferenciado

📊 Encontrados ${{geralCount}} artigos com classificação "Geral" na tabela.

✨ Os ícones "Geral" foram destacados temporariamente!`);
                }}, 1000);
            }}, 500);
        }}
        
        function testODSIcons() {{
            console.log('🧪 Testando ícones ODS...');
            
            // Primeiro desmarca todas
            deselectAll();
            
            // Depois marca apenas ID, Título e ODS
            const testColumns = [1, 3]; // ID e Título
            const odsIndex = odsColumnIndex;
            
            setTimeout(() => {{
                // Ativa colunas base
                testColumns.forEach(index => {{
                    const checkbox = document.getElementById('col_' + index);
                    checkbox.checked = true;
                    toggleColumn(index);
                }});
                
                setTimeout(() => {{
                    // Ativa coluna ODS com destaque
                    if (odsIndex !== undefined) {{
                        const odsCheckbox = document.getElementById('col_' + odsIndex);
                        odsCheckbox.checked = true;
                        toggleColumn(odsIndex);
                        
                        // Destaca a coluna ODS
                        const odsHeader = document.getElementsByTagName('th')[odsIndex];
                        if (odsHeader) {{
                            odsHeader.style.background = 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)';
                            odsHeader.style.transform = 'scale(1.05)';
                            odsHeader.style.boxShadow = '0 4px 15px rgba(231, 76, 60, 0.4)';
                            
                            setTimeout(() => {{
                                odsHeader.style.background = '';
                                odsHeader.style.transform = '';
                                odsHeader.style.boxShadow = '';
                            }}, 3000);
                        }}
                        
                        alert('🧪 Teste de Ícones ODS Completo!\\n\\n🎯 A coluna ODS foi destacada e deve mostrar os ícones oficiais dos Objetivos de Desenvolvimento Sustentável.\\n\\n✨ Passe o mouse sobre os ícones para ver o efeito hover!');
                    }}
                }}, 1000);
            }}, 500);
        }}
        
        function exportToLatex() {{
            const visibleColumns = [];
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]:checked');
            
            checkboxes.forEach(checkbox => {{
                const colIndex = parseInt(checkbox.value);
                const colInfo = columnsInfo[colIndex];
                visibleColumns.push({{
                    index: colIndex, 
                    name: colInfo.name,
                    id: colInfo.id,
                    hasODSIcons: colInfo.is_ods
                }});
            }});
            
            if (visibleColumns.length === 0) {{
                alert('❌ Selecione pelo menos uma coluna para exportar!');
                return;
            }}
            
            const hasODSColumn = visibleColumns.some(col => col.hasODSIcons);
            const odsNote = hasODSColumn ? '\\n🎯 NOTA: A coluna ODS será exportada com ícones para visualização web, mas como texto para LaTeX.' : '';
            
            const message = `✅ Configuração com Ícones ODS para exportação LaTeX:
            
📊 Total de colunas selecionadas: ${{visibleColumns.length}}
📋 Colunas na ordem atual:
${{visibleColumns.map((col, i) => `${{i+1}}. [${{col.index}}] ${{col.name}}${{col.hasODSIcons ? ' 🎯' : ''}}`).join('\\n')}}

🎨 Ícones ODS: ${{hasODSColumn ? 'INCLUÍDOS' : 'Não aplicável'}}${{odsNote}}`;
            
            alert(message);
        }}
        
        // Adiciona efeito especial aos ícones ODS
        document.addEventListener('DOMContentLoaded', function() {{
            // Adiciona listener para ícones ODS
            document.addEventListener('mouseover', function(e) {{
                if (e.target.classList.contains('ods-icon')) {{
                    console.log('🎯 Hover sobre ícone ODS:', e.target.alt);
                }}
            }});
        }});
        
        console.log('🎯 Sistema de ícones ODS carregado e pronto!');
    </script>
</body>
</html>
"""
        
        # Salva o arquivo
        nome_arquivo = "visualizacao_com_icones_ods.html"
        caminho_arquivo = Path(nome_arquivo)
        
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n🎉 VISUALIZAÇÃO COM ÍCONES ODS CRIADA!")
        print(f"📄 Arquivo gerado: {nome_arquivo}")
        print(f"📁 Caminho: {caminho_arquivo.absolute()}")
        
        print(f"\n🎯 FUNCIONALIDADES DOS ÍCONES ODS:")
        print(f"   • Ícones oficiais das Nações Unidas")
        print(f"   • Mapeamento automático de texto para ícones")
        print(f"   • Suporte a múltiplos ODS por artigo")
        print(f"   • Efeitos hover interativos")
        print(f"   • Botão específico 'Mostrar Apenas ODS'")
        print(f"   • Teste dedicado para ícones ODS")
        
        print(f"\n🧪 COMO TESTAR:")
        print(f"   1. Abra o arquivo HTML no navegador")
        print(f"   2. Clique em 'Testar Ícones ODS' para demonstração")
        print(f"   3. Use 'Mostrar Apenas ODS' para foco nos ícones")
        print(f"   4. Passe o mouse sobre os ícones para ver efeitos")
        
        return caminho_arquivo
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def main():
    """Função principal"""
    caminho_excel = "Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx"
    
    if not Path(caminho_excel).exists():
        print(f"❌ Arquivo não encontrado: {caminho_excel}")
        return
    
    # Gera visualização com ícones ODS
    arquivo_html = gerar_visualizacao_com_icones_ods()
    
    if arquivo_html:
        print(f"\n🎨 Pronto! A coluna ODS agora exibe os ícones oficiais!")

if __name__ == "__main__":
    main()
