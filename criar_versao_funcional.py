#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar uma versão SUPER SIMPLES que FUNCIONA
"""

import pandas as pd
from pathlib import Path
import re

def criar_versao_simples_funcional():
    """
    Cria uma versão simples mas 100% funcional
    """
    try:
        # Carrega os dados
        print("🔧 Criando versão SUPER SIMPLES que FUNCIONA...")
        df = pd.read_excel("Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx", sheet_name=0)
        df = df.fillna("")
        
        # Converte para string
        for col in df.columns:
            df[col] = df[col].astype(str)
        
        # Aplica ícones ODS
        def mapear_ods(valor):
            if pd.isna(valor) or valor == "":
                return ""
            
            if str(valor).strip() == "Geral":
                return '<span class="ods-geral">🌍 GERAL</span>'
            
            numeros_ods = re.findall(r'ODS (\d+)', str(valor))
            if numeros_ods:
                icones = []
                for num in numeros_ods:
                    icones.append(f'<img src="Ícones oficiais - ODS/SDG-icon-PT--{num.zfill(2)}-2{"" if num in ["2","3","5","9","10","11","13","16","17"] else "-01"}.png" alt="ODS {num}" class="ods-icon" style="width:40px;height:40px;margin:2px;">')
                return " ".join(icones)
            
            return valor
        
        # Encontra coluna ODS
        coluna_ods = None
        for i, col in enumerate(df.columns):
            if "ODS" in col and "Geral" in col:
                coluna_ods = i
                df[col] = df[col].apply(mapear_ods)
                break
        
        # Gera HTML da tabela
        table_html = df.to_html(classes='table', table_id='dataTable', escape=False, index=False)
        
        html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Visualização FUNCIONAL - Corpus ODS</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .controls {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        
        .buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .btn-primary {{ background: #007bff; color: white; }}
        .btn-danger {{ background: #dc3545; color: white; }}
        .btn-success {{ background: #28a745; color: white; }}
        .btn-warning {{ background: #ffc107; color: black; }}
        
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
        
        .checkboxes {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .checkbox-item {{
            background: white;
            padding: 10px;
            border: 2px solid #e9ecef;
            border-radius: 5px;
            display: flex;
            align-items: center;
        }}
        
        .checkbox-item input {{
            margin-right: 10px;
            transform: scale(1.2);
        }}
        
        .checkbox-item.checked {{
            border-color: #28a745;
            background: #f8fff8;
        }}
        
        .table-container {{
            max-height: 70vh;
            overflow: auto;
            border-radius: 10px;
            border: 1px solid #dee2e6;
        }}
        
        .table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        
        .table th {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .table td {{
            padding: 8px 12px;
            border-bottom: 1px solid #dee2e6;
            vertical-align: top;
            max-width: 300px;
            word-wrap: break-word;
        }}
        
        .table tr:nth-child(even) {{ background: #f8f9fa; }}
        .table tr:hover {{ background: #e3f2fd; }}
        
        .hidden {{ display: none !important; }}
        
        .ods-geral {{
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.8rem;
        }}
        
        .ods-icon {{
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }}
        
        .ods-icon:hover {{
            transform: scale(1.1);
        }}
        
        .status {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Corpus da Análise de Conteúdo</h1>
            <p>Visualização FUNCIONAL com Ícones ODS</p>
        </div>
        
        <div class="status" id="status">
            ✅ Sistema carregado e pronto para uso!
        </div>
        
        <div class="controls">
            <h3>🎛️ Controles de Colunas</h3>
            
            <div class="buttons">
                <button class="btn btn-primary" onclick="selecionarTodas()">
                    ✅ Selecionar Todas
                </button>
                <button class="btn btn-danger" onclick="desmarcarTodas()">
                    ❌ DESMARCAR TODAS
                </button>
                <button class="btn btn-success" onclick="padraoABNT()">
                    📋 Padrão ABNT
                </button>
                <button class="btn btn-warning" onclick="apenasODS()">
                    🎯 Apenas ODS
                </button>
            </div>
            
            <div class="checkboxes" id="checkboxes">
                {self.gerar_checkboxes(df.columns)}
            </div>
        </div>
        
        <div class="table-container">
            {table_html}
        </div>
    </div>

<script>
console.log('🚀 Sistema SUPER SIMPLES iniciado');

// FUNÇÃO SUPER SIMPLES PARA DESMARCAR TODAS
function desmarcarTodas() {{
    console.log('🔴 DESMARCAR TODAS - INICIANDO');
    
    // Atualiza status
    document.getElementById('status').innerHTML = '🔄 Desmarcando todas as colunas...';
    document.getElementById('status').style.background = '#fff3cd';
    document.getElementById('status').style.borderColor = '#ffeaa7';
    document.getElementById('status').style.color = '#856404';
    
    // Pega TODOS os checkboxes
    const checkboxes = document.querySelectorAll('#checkboxes input[type="checkbox"]');
    console.log(`📋 Encontrados ${{checkboxes.length}} checkboxes`);
    
    // Desmarca TODOS
    checkboxes.forEach((checkbox, index) => {{
        checkbox.checked = false;
        const container = checkbox.closest('.checkbox-item');
        container.classList.remove('checked');
        console.log(`☐ Checkbox ${{index}} desmarcado`);
    }});
    
    // Esconde TODAS as colunas da tabela
    const table = document.getElementById('dataTable');
    const headers = table.querySelectorAll('th');
    const rows = table.querySelectorAll('tr');
    
    console.log(`📊 Escondendo ${{headers.length}} cabeçalhos`);
    
    // Esconde todos os cabeçalhos
    headers.forEach((header, index) => {{
        header.classList.add('hidden');
        console.log(`🔒 Cabeçalho ${{index}} ocultado`);
    }});
    
    // Esconde todas as células de todas as linhas
    rows.forEach((row, rowIndex) => {{
        if (rowIndex > 0) {{ // Pula a linha de cabeçalho
            const cells = row.querySelectorAll('td');
            cells.forEach((cell, cellIndex) => {{
                cell.classList.add('hidden');
            }});
        }}
    }});
    
    // Atualiza status final
    setTimeout(() => {{
        const visibleHeaders = table.querySelectorAll('th:not(.hidden)');
        document.getElementById('status').innerHTML = `❌ TODAS AS COLUNAS DESMARCADAS! (${{visibleHeaders.length}} visíveis de ${{headers.length}})`;
        document.getElementById('status').style.background = '#f8d7da';
        document.getElementById('status').style.borderColor = '#f5c6cb';
        document.getElementById('status').style.color = '#721c24';
        console.log('✅ DESMARCAR TODAS - CONCLUÍDO');
    }}, 100);
}}

// FUNÇÃO SUPER SIMPLES PARA SELECIONAR TODAS  
function selecionarTodas() {{
    console.log('🟢 SELECIONAR TODAS - INICIANDO');
    
    document.getElementById('status').innerHTML = '🔄 Selecionando todas as colunas...';
    document.getElementById('status').style.background = '#d1ecf1';
    document.getElementById('status').style.borderColor = '#bee5eb';
    document.getElementById('status').style.color = '#0c5460';
    
    const checkboxes = document.querySelectorAll('#checkboxes input[type="checkbox"]');
    console.log(`📋 Selecionando ${{checkboxes.length}} checkboxes`);
    
    checkboxes.forEach((checkbox, index) => {{
        checkbox.checked = true;
        const container = checkbox.closest('.checkbox-item');
        container.classList.add('checked');
        console.log(`☑️ Checkbox ${{index}} marcado`);
    }});
    
    const table = document.getElementById('dataTable');
    const headers = table.querySelectorAll('th');
    const rows = table.querySelectorAll('tr');
    
    console.log(`📊 Mostrando ${{headers.length}} cabeçalhos`);
    
    headers.forEach((header, index) => {{
        header.classList.remove('hidden');
        console.log(`👁️ Cabeçalho ${{index}} mostrado`);
    }});
    
    rows.forEach((row, rowIndex) => {{
        if (rowIndex > 0) {{
            const cells = row.querySelectorAll('td');
            cells.forEach((cell, cellIndex) => {{
                cell.classList.remove('hidden');
            }});
        }}
    }});
    
    setTimeout(() => {{
        const visibleHeaders = table.querySelectorAll('th:not(.hidden)');
        document.getElementById('status').innerHTML = `✅ TODAS AS COLUNAS SELECIONADAS! (${{visibleHeaders.length}} visíveis)`;
        document.getElementById('status').style.background = '#d4edda';
        document.getElementById('status').style.borderColor = '#c3e6cb';
        document.getElementById('status').style.color = '#155724';
        console.log('✅ SELECIONAR TODAS - CONCLUÍDO');
    }}, 100);
}}

function alternarColuna(index) {{
    const checkbox = document.getElementById('col_' + index);
    const isChecked = checkbox.checked;
    const container = checkbox.closest('.checkbox-item');
    
    console.log(`🔄 Alternando coluna ${{index}}: ${{isChecked ? 'MOSTRAR' : 'OCULTAR'}}`);
    
    if (isChecked) {{
        container.classList.add('checked');
    }} else {{
        container.classList.remove('checked');
    }}
    
    const table = document.getElementById('dataTable');
    const headers = table.querySelectorAll('th');
    const rows = table.querySelectorAll('tr');
    
    if (headers[index]) {{
        if (isChecked) {{
            headers[index].classList.remove('hidden');
        }} else {{
            headers[index].classList.add('hidden');
        }}
    }}
    
    rows.forEach((row, rowIndex) => {{
        if (rowIndex > 0) {{
            const cells = row.querySelectorAll('td');
            if (cells[index]) {{
                if (isChecked) {{
                    cells[index].classList.remove('hidden');
                }} else {{
                    cells[index].classList.add('hidden');
                }}
            }}
        }}
    }});
    
    // Atualiza contador
    setTimeout(() => {{
        const visibleHeaders = table.querySelectorAll('th:not(.hidden)');
        document.getElementById('status').innerHTML = `📊 ${{visibleHeaders.length}} colunas visíveis de ${{headers.length}} total`;
        document.getElementById('status').style.background = '#d4edda';
        document.getElementById('status').style.borderColor = '#c3e6cb';
        document.getElementById('status').style.color = '#155724';
    }}, 50);
}}

function padraoABNT() {{
    const padroes = ['ID', 'Autores', 'Título', 'Ano', 'Periódico', 'ODS', 'Aspecto Principal'];
    const checkboxes = document.querySelectorAll('#checkboxes input[type="checkbox"]');
    
    checkboxes.forEach((checkbox, index) => {{
        const label = checkbox.nextElementSibling.textContent;
        const shouldCheck = padroes.some(p => label.includes(p));
        checkbox.checked = shouldCheck;
        alternarColuna(index);
    }});
}}

function apenasODS() {{
    const essenciais = ['ID', 'Título', 'ODS'];
    const checkboxes = document.querySelectorAll('#checkboxes input[type="checkbox"]');
    
    checkboxes.forEach((checkbox, index) => {{
        const label = checkbox.nextElementSibling.textContent;
        const shouldCheck = essenciais.some(p => label.includes(p));
        checkbox.checked = shouldCheck;
        alternarColuna(index);
    }});
}}

console.log('✅ Todas as funções carregadas. DESMARCAR TODAS deve funcionar!');
</script>
</body>
</html>'''
        
        return html_content
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def gerar_checkboxes(colunas):
    """Gera checkboxes para as colunas"""
    html = ""
    for i, col in enumerate(colunas):
        checked = "checked" if i < 7 else ""
        checked_class = "checked" if i < 7 else ""
        emoji = "🎯 " if "ODS" in col else ""
        
        html += f'''
        <div class="checkbox-item {checked_class}">
            <input type="checkbox" id="col_{i}" {checked} onchange="alternarColuna({i})">
            <label for="col_{i}">{emoji}[{i}] {col[:40]}{"..." if len(col) > 40 else ""}</label>
        </div>'''
    
    return html

# Patch para self
def create_html():
    df = pd.read_excel("Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx", sheet_name=0)
    df = df.fillna("")
    
    for col in df.columns:
        df[col] = df[col].astype(str)
    
    def mapear_ods(valor):
        if pd.isna(valor) or valor == "":
            return ""
        
        if str(valor).strip() == "Geral":
            return '<span class="ods-geral">🌍 GERAL</span>'
        
        numeros_ods = re.findall(r'ODS (\d+)', str(valor))
        if numeros_ods:
            icones = []
            for num in numeros_ods:
                extensao = "" if num in ["2","3","5","9","10","11","13","16","17"] else "-01"
                icones.append(f'<img src="Ícones oficiais - ODS/SDG-icon-PT--{num.zfill(2)}-2{extensao}.png" alt="ODS {num}" class="ods-icon" style="width:40px;height:40px;margin:2px;">')
            return " ".join(icones)
        
        return valor
    
    for i, col in enumerate(df.columns):
        if "ODS" in col and "Geral" in col:
            df[col] = df[col].apply(mapear_ods)
            break
    
    table_html = df.to_html(classes='table', table_id='dataTable', escape=False, index=False)
    checkboxes_html = gerar_checkboxes(df.columns)
    
    html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Visualização FUNCIONAL - Corpus ODS</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .controls {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        
        .buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .btn-primary {{ background: #007bff; color: white; }}
        .btn-danger {{ background: #dc3545; color: white; }}
        .btn-success {{ background: #28a745; color: white; }}
        .btn-warning {{ background: #ffc107; color: black; }}
        
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
        
        .checkboxes {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .checkbox-item {{
            background: white;
            padding: 10px;
            border: 2px solid #e9ecef;
            border-radius: 5px;
            display: flex;
            align-items: center;
        }}
        
        .checkbox-item input {{
            margin-right: 10px;
            transform: scale(1.2);
        }}
        
        .checkbox-item.checked {{
            border-color: #28a745;
            background: #f8fff8;
        }}
        
        .table-container {{
            max-height: 70vh;
            overflow: auto;
            border-radius: 10px;
            border: 1px solid #dee2e6;
        }}
        
        .table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        
        .table th {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .table td {{
            padding: 8px 12px;
            border-bottom: 1px solid #dee2e6;
            vertical-align: top;
            max-width: 300px;
            word-wrap: break-word;
        }}
        
        .table tr:nth-child(even) {{ background: #f8f9fa; }}
        .table tr:hover {{ background: #e3f2fd; }}
        
        .hidden {{ display: none !important; }}
        
        .ods-geral {{
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.8rem;
        }}
        
        .ods-icon {{
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }}
        
        .ods-icon:hover {{
            transform: scale(1.1);
        }}
        
        .status {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Corpus da Análise de Conteúdo</h1>
            <p>Visualização FUNCIONAL com Ícones ODS</p>
        </div>
        
        <div class="status" id="status">
            ✅ Sistema carregado e pronto para uso!
        </div>
        
        <div class="controls">
            <h3>🎛️ Controles de Colunas</h3>
            
            <div class="buttons">
                <button class="btn btn-primary" onclick="selecionarTodas()">
                    ✅ Selecionar Todas
                </button>
                <button class="btn btn-danger" onclick="desmarcarTodas()">
                    ❌ DESMARCAR TODAS
                </button>
                <button class="btn btn-success" onclick="padraoABNT()">
                    📋 Padrão ABNT
                </button>
                <button class="btn btn-warning" onclick="apenasODS()">
                    🎯 Apenas ODS
                </button>
            </div>
            
            <div class="checkboxes" id="checkboxes">
                {checkboxes_html}
            </div>
        </div>
        
        <div class="table-container">
            {table_html}
        </div>
    </div>

<script>
console.log('🚀 Sistema SUPER SIMPLES iniciado');

// FUNÇÃO SUPER SIMPLES PARA DESMARCAR TODAS
function desmarcarTodas() {{
    console.log('🔴 DESMARCAR TODAS - INICIANDO');
    
    // Atualiza status
    document.getElementById('status').innerHTML = '🔄 Desmarcando todas as colunas...';
    document.getElementById('status').style.background = '#fff3cd';
    document.getElementById('status').style.borderColor = '#ffeaa7';
    document.getElementById('status').style.color = '#856404';
    
    // Pega TODOS os checkboxes
    const checkboxes = document.querySelectorAll('#checkboxes input[type="checkbox"]');
    console.log(`📋 Encontrados ${{checkboxes.length}} checkboxes`);
    
    // Desmarca TODOS
    checkboxes.forEach((checkbox, index) => {{
        checkbox.checked = false;
        const container = checkbox.closest('.checkbox-item');
        container.classList.remove('checked');
        console.log(`☐ Checkbox ${{index}} desmarcado`);
    }});
    
    // Esconde TODAS as colunas da tabela
    const table = document.getElementById('dataTable');
    const headers = table.querySelectorAll('th');
    const rows = table.querySelectorAll('tr');
    
    console.log(`📊 Escondendo ${{headers.length}} cabeçalhos`);
    
    // Esconde todos os cabeçalhos
    headers.forEach((header, index) => {{
        header.classList.add('hidden');
        console.log(`🔒 Cabeçalho ${{index}} ocultado`);
    }});
    
    // Esconde todas as células de todas as linhas
    rows.forEach((row, rowIndex) => {{
        if (rowIndex > 0) {{ // Pula a linha de cabeçalho
            const cells = row.querySelectorAll('td');
            cells.forEach((cell, cellIndex) => {{
                cell.classList.add('hidden');
            }});
        }}
    }});
    
    // Atualiza status final
    setTimeout(() => {{
        const visibleHeaders = table.querySelectorAll('th:not(.hidden)');
        document.getElementById('status').innerHTML = `❌ TODAS AS COLUNAS DESMARCADAS! (${{visibleHeaders.length}} visíveis de ${{headers.length}})`;
        document.getElementById('status').style.background = '#f8d7da';
        document.getElementById('status').style.borderColor = '#f5c6cb';
        document.getElementById('status').style.color = '#721c24';
        console.log('✅ DESMARCAR TODAS - CONCLUÍDO');
    }}, 100);
}}

// FUNÇÃO SUPER SIMPLES PARA SELECIONAR TODAS  
function selecionarTodas() {{
    console.log('🟢 SELECIONAR TODAS - INICIANDO');
    
    document.getElementById('status').innerHTML = '🔄 Selecionando todas as colunas...';
    document.getElementById('status').style.background = '#d1ecf1';
    document.getElementById('status').style.borderColor = '#bee5eb';
    document.getElementById('status').style.color = '#0c5460';
    
    const checkboxes = document.querySelectorAll('#checkboxes input[type="checkbox"]');
    console.log(`📋 Selecionando ${{checkboxes.length}} checkboxes`);
    
    checkboxes.forEach((checkbox, index) => {{
        checkbox.checked = true;
        const container = checkbox.closest('.checkbox-item');
        container.classList.add('checked');
        console.log(`☑️ Checkbox ${{index}} marcado`);
    }});
    
    const table = document.getElementById('dataTable');
    const headers = table.querySelectorAll('th');
    const rows = table.querySelectorAll('tr');
    
    console.log(`📊 Mostrando ${{headers.length}} cabeçalhos`);
    
    headers.forEach((header, index) => {{
        header.classList.remove('hidden');
        console.log(`👁️ Cabeçalho ${{index}} mostrado`);
    }});
    
    rows.forEach((row, rowIndex) => {{
        if (rowIndex > 0) {{
            const cells = row.querySelectorAll('td');
            cells.forEach((cell, cellIndex) => {{
                cell.classList.remove('hidden');
            }});
        }}
    }});
    
    setTimeout(() => {{
        const visibleHeaders = table.querySelectorAll('th:not(.hidden)');
        document.getElementById('status').innerHTML = `✅ TODAS AS COLUNAS SELECIONADAS! (${{visibleHeaders.length}} visíveis)`;
        document.getElementById('status').style.background = '#d4edda';
        document.getElementById('status').style.borderColor = '#c3e6cb';
        document.getElementById('status').style.color = '#155724';
        console.log('✅ SELECIONAR TODAS - CONCLUÍDO');
    }}, 100);
}}

function alternarColuna(index) {{
    const checkbox = document.getElementById('col_' + index);
    const isChecked = checkbox.checked;
    const container = checkbox.closest('.checkbox-item');
    
    console.log(`🔄 Alternando coluna ${{index}}: ${{isChecked ? 'MOSTRAR' : 'OCULTAR'}}`);
    
    if (isChecked) {{
        container.classList.add('checked');
    }} else {{
        container.classList.remove('checked');
    }}
    
    const table = document.getElementById('dataTable');
    const headers = table.querySelectorAll('th');
    const rows = table.querySelectorAll('tr');
    
    if (headers[index]) {{
        if (isChecked) {{
            headers[index].classList.remove('hidden');
        }} else {{
            headers[index].classList.add('hidden');
        }}
    }}
    
    rows.forEach((row, rowIndex) => {{
        if (rowIndex > 0) {{
            const cells = row.querySelectorAll('td');
            if (cells[index]) {{
                if (isChecked) {{
                    cells[index].classList.remove('hidden');
                }} else {{
                    cells[index].classList.add('hidden');
                }}
            }}
        }}
    }});
    
    // Atualiza contador
    setTimeout(() => {{
        const visibleHeaders = table.querySelectorAll('th:not(.hidden)');
        document.getElementById('status').innerHTML = `📊 ${{visibleHeaders.length}} colunas visíveis de ${{headers.length}} total`;
        document.getElementById('status').style.background = '#d4edda';
        document.getElementById('status').style.borderColor = '#c3e6cb';
        document.getElementById('status').style.color = '#155724';
    }}, 50);
}}

function padraoABNT() {{
    const padroes = ['ID', 'Autores', 'Título', 'Ano', 'Periódico', 'ODS', 'Aspecto Principal'];
    const checkboxes = document.querySelectorAll('#checkboxes input[type="checkbox"]');
    
    checkboxes.forEach((checkbox, index) => {{
        const label = checkbox.nextElementSibling.textContent;
        const shouldCheck = padroes.some(p => label.includes(p));
        checkbox.checked = shouldCheck;
        alternarColuna(index);
    }});
}}

function apenasODS() {{
    const essenciais = ['ID', 'Título', 'ODS'];
    const checkboxes = document.querySelectorAll('#checkboxes input[type="checkbox"]');
    
    checkboxes.forEach((checkbox, index) => {{
        const label = checkbox.nextElementSibling.textContent;
        const shouldCheck = essenciais.some(p => label.includes(p));
        checkbox.checked = shouldCheck;
        alternarColuna(index);
    }});
}}

console.log('✅ Todas as funções carregadas. DESMARCAR TODAS deve funcionar!');
</script>
</body>
</html>'''
    
    return html_content

def main():
    print("🔥 CRIANDO VERSÃO QUE VAI FUNCIONAR 100%!")
    
    html_content = create_html()
    
    with open("visualizacao_FUNCIONAL.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ CRIADO: visualizacao_FUNCIONAL.html")
    print("🎯 Esta versão é SUPER SIMPLES e VAI FUNCIONAR!")
    print("❌ O botão DESMARCAR TODAS vai funcionar perfeitamente!")

if __name__ == "__main__":
    main()
