#!/usr/bin/env python3
"""
Script para processar dados atualizados do Excel e gerar JavaScript
Arquivo: Análise de Conteúdo - Luciano 22_06.xlsx
"""

import pandas as pd
import json
import re
import os

def processar_dados_atualizados():
    arquivo_excel = 'Análise de Conteúdo - Luciano 22_06.xlsx'
    
    print("🔄 PROCESSAMENTO DE DADOS ATUALIZADOS")
    print("=" * 50)
    
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_excel):
        print(f"❌ ERRO: Arquivo {arquivo_excel} não encontrado!")
        return False
    
    try:
        # Carregar dados do Excel
        print(f"📊 Carregando dados de {arquivo_excel}...")
        df = pd.read_excel(arquivo_excel)
        
        print(f"✅ Dados carregados: {len(df)} registros")
        print(f"📋 Colunas encontradas: {len(df.columns)}")
        
        # Mostrar colunas
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # Tratar valores NaN
        df = df.fillna('')
        
        # Converter DataFrame para lista de dicionários
        dados = df.to_dict('records')
        
        # Converter para JavaScript
        print(f"\n🔧 Convertendo para JavaScript...")
        
        js_content = "const data = [\n"
        for i, registro in enumerate(dados):
            js_content += "  {\n"
            for coluna, valor in registro.items():
                # Escapar aspas e quebras de linha
                valor_str = str(valor).replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
                js_content += f'    "{coluna}": "{valor_str}",\n'
            js_content = js_content.rstrip(',\n') + '\n'
            js_content += "  }"
            if i < len(dados) - 1:
                js_content += ","
            js_content += "\n"
        js_content += "];\n"
        
        # Salvar arquivo JavaScript
        with open('dados_javascript.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"✅ Arquivo dados_javascript.js gerado com sucesso!")
        print(f"📊 {len(dados)} registros convertidos")
        
        # Gerar relatório das colunas
        colunas_encontradas = list(df.columns)
        relatorio = {
            "arquivo_fonte": arquivo_excel,
            "total_registros": len(df),
            "total_colunas": len(df.columns),
            "colunas": colunas_encontradas,
            "atualizacao": "2025-06-22"
        }
        
        with open('relatorio_atualizacao.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Relatório salvo em relatorio_atualizacao.json")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

if __name__ == "__main__":
    processar_dados_atualizados()
