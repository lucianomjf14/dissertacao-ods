#!/usr/bin/env python3
"""
Script para extrair dados completos do arquivo NOVO e gerar dados com ODS para as métricas
MIGRAÇÃO: Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx → Análise de Conteúdo - Luciano 22_06.xlsx
"""

import pandas as pd
import json
import re
import os

def processar_dados_ods_migrado():
    # Configuração de arquivos
    arquivo_novo = 'Análise de Conteúdo - Luciano 22_06.xlsx'
    arquivo_antigo = 'Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx'
    
    print("🔄 MIGRAÇÃO DE FONTE DE DADOS ODS/CSC")
    print("=" * 50)
    
    # Verificar se o arquivo novo existe
    if not os.path.exists(arquivo_novo):
        print(f"❌ Arquivo novo não encontrado: {arquivo_novo}")
        print(f"🔙 Usando arquivo antigo: {arquivo_antigo}")
        arquivo_a_usar = arquivo_antigo
    else:
        print(f"✅ Usando arquivo novo: {arquivo_novo}")
        arquivo_a_usar = arquivo_novo
    
    # Ler o arquivo Excel
    try:
        df = pd.read_excel(arquivo_a_usar)
        print(f"✅ Arquivo Excel carregado: {len(df)} registros")
        print(f"📊 Colunas: {len(df.columns)}")
        
        # Mapeamento de colunas antigas → novas
        mapeamento_colunas = {
            'Ano': 'Ano de Publicação',
            'ODS (Geral / Específico)': 'ODS Mencionados pelos Autores'
        }
        
        # Mostrar colunas disponíveis
        print(f"\n📋 Colunas disponíveis no arquivo:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # Criar dados JSON com flags para cada ODS
        dados_json = []
        
        for index, row in df.iterrows():
            # Converter para dict
            registro = row.to_dict()
            
            # Mapear colunas antigas para as novas estruturas
            # Se usar arquivo novo, aplicar mapeamento reverso para compatibilidade
            if arquivo_a_usar == arquivo_novo:
                # Criar aliases para compatibilidade com código existente
                if 'Ano de Publicação' in registro:
                    registro['Ano'] = registro['Ano de Publicação']
                if 'ODS Mencionados pelos Autores' in registro:
                    registro['ODS (Geral / Específico)'] = registro['ODS Mencionados pelos Autores']
            
            # Adicionar flags para cada ODS baseado na coluna ODS
            ods_coluna = 'ODS (Geral / Específico)' if 'ODS (Geral / Específico)' in registro else 'ODS Mencionados pelos Autores'
            ods_valor = str(registro.get(ods_coluna, ''))
            
            # Adicionar flags individuais para cada ODS
            # Usando regex para busca precisa e evitar confusão entre ODS 1 e ODS 11
            registro['ODS 1'] = 'x' if re.search(r'\bODS 1\b', ods_valor) else ''
            registro['ODS 2'] = 'x' if re.search(r'\bODS 2\b', ods_valor) else ''
            registro['ODS 3'] = 'x' if re.search(r'\bODS 3\b', ods_valor) else ''
            registro['ODS 4'] = 'x' if re.search(r'\bODS 4\b', ods_valor) else ''
            registro['ODS 5'] = 'x' if re.search(r'\bODS 5\b', ods_valor) else ''
            registro['ODS 6'] = 'x' if re.search(r'\bODS 6\b', ods_valor) else ''
            registro['ODS 7'] = 'x' if re.search(r'\bODS 7\b', ods_valor) else ''
            registro['ODS 8'] = 'x' if re.search(r'\bODS 8\b', ods_valor) else ''
            registro['ODS 9'] = 'x' if re.search(r'\bODS 9\b', ods_valor) else ''
            registro['ODS 10'] = 'x' if re.search(r'\bODS 10\b', ods_valor) else ''
            registro['ODS 11'] = 'x' if re.search(r'\bODS 11\b', ods_valor) else ''
            registro['ODS 12'] = 'x' if re.search(r'\bODS 12\b', ods_valor) else ''
            registro['ODS 13'] = 'x' if re.search(r'\bODS 13\b', ods_valor) else ''
            registro['ODS 14'] = 'x' if re.search(r'\bODS 14\b', ods_valor) else ''
            registro['ODS 15'] = 'x' if re.search(r'\bODS 15\b', ods_valor) else ''
            registro['ODS 16'] = 'x' if re.search(r'\bODS 16\b', ods_valor) else ''
            registro['ODS 17'] = 'x' if re.search(r'\bODS 17\b', ods_valor) else ''
            registro['Geral'] = 'x' if re.search(r'\bGeral\b', ods_valor) else ''
            
            # Limpar valores NaN
            for key, value in registro.items():
                if pd.isna(value):
                    registro[key] = ''
                else:
                    registro[key] = str(value)
            
            dados_json.append(registro)
        
        # Salvar dados completos em arquivo
        with open('dados_completos_ods.json', 'w', encoding='utf-8') as f:
            json.dump(dados_json, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Dados processados e salvos: {len(dados_json)} registros")
        
        # Calcular estatísticas dos ODS
        estatisticas = {}
        ods_list = ['ODS 1', 'ODS 2', 'ODS 3', 'ODS 4', 'ODS 5', 'ODS 6', 'ODS 7', 'ODS 8', 'ODS 9', 'ODS 10', 'ODS 11', 'ODS 12', 'ODS 13', 'ODS 14', 'ODS 15', 'ODS 16', 'ODS 17', 'Geral']
        
        for ods in ods_list:
            count = sum(1 for item in dados_json if item.get(ods) == 'x')
            percentage = (count / len(dados_json)) * 100 if dados_json else 0
            estatisticas[ods] = {
                'count': count,
                'percentage': round(percentage, 1)
            }
        
        print("\n📊 ESTATÍSTICAS DOS ODS:")
        print("-" * 50)
        for ods, stats in estatisticas.items():
            print(f"{ods:<10} {stats['count']:>3} estudos ({stats['percentage']:>5.1f}%)")
        
        # Gerar o JavaScript com os dados
        js_code = f"const data = {json.dumps(dados_json, ensure_ascii=False, indent=2)};"
        
        with open('dados_javascript.js', 'w', encoding='utf-8') as f:
            f.write(js_code)
        
        print(f"\n✅ Arquivo JavaScript gerado: dados_javascript.js")
        
        # Relatório de migração
        relatorio_migracao = {
            'arquivo_usado': arquivo_a_usar,
            'data_migracao': pd.Timestamp.now().isoformat(),
            'registros_processados': len(dados_json),
            'colunas_mapeadas': mapeamento_colunas if arquivo_a_usar == arquivo_novo else {},
            'estatisticas_ods': estatisticas
        }
        
        with open('relatorio_migracao_processamento.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio_migracao, f, ensure_ascii=False, indent=2)
        
        print(f"📋 Relatório de migração salvo: relatorio_migracao_processamento.json")
        
        return dados_json, estatisticas
        
    except Exception as e:
        print(f"❌ Erro ao processar dados: {e}")
        return None, None

if __name__ == "__main__":
    dados, stats = processar_dados_ods_migrado()
