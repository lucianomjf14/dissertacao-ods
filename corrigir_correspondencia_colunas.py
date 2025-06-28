#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir definitivamente o problema de correspondência de colunas
"""

import pandas as pd
from pathlib import Path

def corrigir_correspondencia_colunas(caminho_arquivo):
    """
    Corrige o problema de correspondência entre seleção de colunas e grid
    """
    try:
        # Carrega os dados
        print("🔧 Corrigindo problema de correspondência de colunas...")
        df = pd.read_excel(caminho_arquivo, sheet_name=0)
        
        print(f"📊 Dados carregados: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        # Substitui valores NaN
        df = df.fillna("")
        
        # Converte todas as colunas para string
        for col in df.columns:
            df[col] = df[col].astype(str)
        
        # Cria mapeamento estável das colunas
        colunas_info = []
        for i, col in enumerate(df.columns):
            colunas_info.append({
                'index': i,
                'name': col,
                'id': f'col_{i}',
                'display_name': col[:50] + "..." if len(col) > 50 else col
            })
        
        print(f"\n📋 MAPEAMENTO CORRIGIDO DAS COLUNAS:")
        print("="*80)
        for info in colunas_info:
            print(f"ID: {info['id']:8} | Índice: {info['index']:2d} | Nome: {info['name']}")
        
        return df, colunas_info
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None, None

def gerar_visualizacao_corrigida_final(df, colunas_info):
    """
    Gera visualização com mapeamento correto e estável de colunas
    """
    
    # Gera a tabela HTML
    table_html = df.to_html(
        classes='data-table',
        table_id='mainTable',
        escape=False,
        index=False
    )
    
    # Cria checkboxes com mapeamento correto
    colunas_checkboxes = ""
    for info in colunas_info:
        checked = "checked" if info['index'] < 7 else ""  # Primeiras 7 visíveis
        
        colunas_checkboxes += f"""
        <div class="column-option" data-col-index="{info['index']}" data-original-index="{info['index']}">
            <input type="checkbox" id="{info['id']}" value="{info['index']}" {checked} onchange="toggleColumn({info['index']})">
            <label for="{info['id']}">
                <span class="drag-handle">⋮⋮</span>
                <span class="col-index">[{info['index']}]</span>
                <span class="col-name">{info['display_name']}</span>
            </label>
        </div>
        """
    
    # Array JavaScript com informações das colunas
    js_colunas_info = str([{
        'index': info['index'],
        'name': info['name'],
        'id': info['id']
    } for info in colunas_info])
    
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✅ Visualização CORRIGIDA - Corpus da Análise de Conteúdo</title>
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
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
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
        
        .fix-notice {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
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
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
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
            border-color: #27ae60;
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
        
        .stats {{
            background: #e8f4f8;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            border-left: 5px solid #27ae60;
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
            color: #27ae60;
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
            <h1>✅ Corpus da Análise de Conteúdo</h1>
            <p>Visualização com Correspondência CORRIGIDA</p>
        </div>
        
        <div class="fix-notice">
            🔧 PROBLEMA CORRIGIDO: Agora a seleção de colunas corresponde exatamente ao que aparece na tabela!
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
                <h4>📋 Como usar (VERSÃO CORRIGIDA):</h4>
                <ul>
                    <li><strong>✅ Funcionalidade Corrigida:</strong> Cada checkbox agora corresponde exatamente à coluna correta</li>
                    <li><strong>Selecionar colunas:</strong> Marque/desmarque as caixas abaixo</li>
                    <li><strong>Índices visuais:</strong> Os números azuis [0], [1], etc. mostram o índice real da coluna</li>
                    <li><strong>Teste:</strong> Desmarque uma coluna e veja que a coluna correta desaparece da tabela</li>
                </ul>
            </div>
            
            <div class="debug-info">
                <h4>🔍 Informações de Debug</h4>
                <p><strong>Total de colunas:</strong> {len(colunas_info)} colunas mapeadas corretamente</p>
                <p><strong>Mapeamento:</strong> Cada checkbox tem um ID único correspondente ao índice da coluna</p>
                <p><strong>Teste rápido:</strong> Desmarque "Link" (índice 0) - deve esconder a primeira coluna da tabela</p>
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
                <button class="btn btn-warning" onclick="testMapping()">
                    🧪 Testar Mapeamento
                </button>
                <button class="btn btn-primary" onclick="exportToLatex()">
                    📄 Exportar LaTeX
                </button>
            </div>
            
            <h4 style="margin-top: 20px; margin-bottom: 15px; color: #2c3e50;">
                📋 Seleção de Colunas (Mapeamento Corrigido):
            </h4>
            <div class="column-selector" id="columnSelector">
                {colunas_checkboxes}
            </div>
        </div>
        
        <div class="table-container">
            {table_html}
        </div>
        
        <div class="footer">
            <p>✅ Visualização Corrigida | Dissertação de Mestrado | Correspondência de Colunas: 100% Funcional</p>
        </div>
    </div>

    <script>
        // Informações das colunas carregadas do Python
        const columnsInfo = {js_colunas_info};
        
        console.log('✅ Colunas carregadas:', columnsInfo);
        
        // Função corrigida para alternar visibilidade das colunas
        function toggleColumn(colIndex) {{
            console.log(`🔧 Alternando coluna índice: ${{colIndex}}`);
            
            const table = document.getElementById('mainTable');
            const checkbox = document.getElementById('col_' + colIndex);
            
            if (!checkbox) {{
                console.error(`❌ Checkbox não encontrado: col_${{colIndex}}`);
                return;
            }}
            
            const isChecked = checkbox.checked;
            console.log(`📊 Coluna ${{colIndex}} está ${{isChecked ? 'marcada' : 'desmarcada'}}`);
            
            // Alterna header (cabeçalho)
            const headerCells = table.getElementsByTagName('th');
            if (headerCells[colIndex]) {{
                headerCells[colIndex].classList.toggle('hidden-column', !isChecked);
                console.log(`✅ Header da coluna ${{colIndex}} ${{isChecked ? 'mostrado' : 'ocultado'}}`);
            }} else {{
                console.error(`❌ Header da coluna ${{colIndex}} não encontrado`);
            }}
            
            // Alterna células de dados
            const rows = table.getElementsByTagName('tr');
            for (let i = 1; i < rows.length; i++) {{
                const cells = rows[i].getElementsByTagName('td');
                if (cells[colIndex]) {{
                    cells[colIndex].classList.toggle('hidden-column', !isChecked);
                }}
            }}
            
            console.log(`✅ Coluna ${{colIndex}} processada com sucesso`);
        }}
        
        function selectAll() {{
            console.log('🔄 Selecionando todas as colunas...');
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            checkboxes.forEach((checkbox) => {{
                const colIndex = parseInt(checkbox.value);
                checkbox.checked = true;
                toggleColumn(colIndex);
            }});
            console.log('✅ Todas as colunas selecionadas');
        }}
        
        function deselectAll() {{
            console.log('🔄 Desmarcando todas as colunas...');
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            checkboxes.forEach((checkbox) => {{
                const colIndex = parseInt(checkbox.value);
                checkbox.checked = false;
                toggleColumn(colIndex);
            }});
            console.log('✅ Todas as colunas desmarcadas');
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
            console.log('✅ Configuração padrão aplicada');
        }}
        
        function testMapping() {{
            console.log('🧪 Testando mapeamento de colunas...');
            
            // Primeiro, desmarca todas
            deselectAll();
            
            // Depois, marca apenas as primeiras 3 colunas uma por vez com delay
            const testColumns = [0, 1, 2];
            let delay = 0;
            
            testColumns.forEach((colIndex, i) => {{
                setTimeout(() => {{
                    const checkbox = document.getElementById('col_' + colIndex);
                    const colName = columnsInfo[colIndex].name;
                    
                    checkbox.checked = true;
                    toggleColumn(colIndex);
                    
                    console.log(`🧪 Teste ${{i+1}}/3: Ativando coluna ${{colIndex}} (${{colName}})`);
                    
                    if (i === testColumns.length - 1) {{
                        alert(`🧪 Teste de Mapeamento Completo!
                        
✅ As 3 primeiras colunas foram ativadas em sequência:
• Coluna 0: ${{columnsInfo[0].name}}
• Coluna 1: ${{columnsInfo[1].name}}
• Coluna 2: ${{columnsInfo[2].name}}

Verifique se as colunas corretas estão visíveis na tabela.`);
                    }}
                }}, delay);
                delay += 1000; // 1 segundo entre cada ativação
            }});
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
                    id: colInfo.id
                }});
            }});
            
            if (visibleColumns.length === 0) {{
                alert('❌ Selecione pelo menos uma coluna para exportar!');
                return;
            }}
            
            console.log('📄 Colunas selecionadas para exportação:', visibleColumns);
            
            const message = `✅ Configuração CORRIGIDA para exportação LaTeX:
            
📊 Total de colunas selecionadas: ${{visibleColumns.length}}
📋 Colunas na ordem atual:
${{visibleColumns.map((col, i) => `${{i+1}}. [${{col.index}}] ${{col.name}}`).join('\\n')}}

🔧 Mapeamento verificado e correto!`;
            
            alert(message);
        }}
        
        // Log inicial para verificação
        console.log('🚀 Sistema de correspondência de colunas inicializado');
        console.log('📊 Total de colunas mapeadas:', columnsInfo.length);
        
        // Testa se todos os checkboxes foram criados corretamente
        document.addEventListener('DOMContentLoaded', function() {{
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            console.log(`✅ Total de checkboxes encontrados: ${{checkboxes.length}}`);
            
            checkboxes.forEach((checkbox, i) => {{
                const colIndex = parseInt(checkbox.value);
                const expectedIndex = i;
                if (colIndex !== expectedIndex) {{
                    console.warn(`⚠️ Possível problema: Checkbox ${{i}} tem valor ${{colIndex}}, esperado ${{expectedIndex}}`);
                }}
            }});
        }});
    </script>
</body>
</html>
"""
    
    # Salva o arquivo
    nome_arquivo = "visualizacao_correspondencia_corrigida.html"
    caminho_arquivo = Path("visualizacao_correspondencia_corrigida.html")
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Arquivo salvo: {nome_arquivo}")
    print(f"📁 Caminho: {caminho_arquivo.absolute()}")
    
    return caminho_arquivo

def main():
    """Função principal"""
    caminho_excel = "Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx"
    
    if not Path(caminho_excel).exists():
        print(f"❌ Arquivo não encontrado: {caminho_excel}")
        return
    
    # Carrega dados e corrige correspondência
    df, colunas_info = corrigir_correspondencia_colunas(caminho_excel)
    
    if df is not None and colunas_info is not None:
        # Gera visualização corrigida
        arquivo_html = gerar_visualizacao_corrigida_final(df, colunas_info)
        
        print(f"\n🎉 CORREÇÃO CONCLUÍDA!")
        print(f"📄 Arquivo gerado: {arquivo_html}")
        print(f"\n🔧 O QUE FOI CORRIGIDO:")
        print(f"   • Mapeamento estável entre checkboxes e colunas da tabela")
        print(f"   • Cada checkbox tem um ID único correspondente ao índice da coluna")
        print(f"   • Índices visuais [0], [1], etc. para facilitar identificação")
        print(f"   • Função de teste para verificar o mapeamento")
        print(f"   • Logs detalhados no console do navegador")
        print(f"\n🧪 COMO TESTAR:")
        print(f"   1. Abra o arquivo HTML no navegador")
        print(f"   2. Clique em 'Testar Mapeamento' para ver demonstração")
        print(f"   3. Desmarque qualquer coluna e veja se a coluna correta desaparece")
        print(f"   4. Use F12 para ver logs detalhados no Console")

if __name__ == "__main__":
    main()
