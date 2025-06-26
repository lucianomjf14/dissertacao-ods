#!/usr/bin/env python3
"""
Script para extrair dados completos do arquivo original e gerar dados com ODS para as métricas
"""

import pandas as pd
import json
import re

def processar_dados_ods():
    # Ler o arquivo Excel original
    try:
        df = pd.read_excel('Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx')
        print(f"✅ Arquivo Excel carregado: {len(df)} registros")
        
        # Criar dados JSON com flags para cada ODS
        dados_json = []
        
        for index, row in df.iterrows():
            # Converter para dict
            registro = row.to_dict()
            
            # Adicionar flags para cada ODS baseado na coluna "ODS (Geral / Específico)"
            ods_valor = str(registro.get('ODS (Geral / Específico)', ''))            # Adicionar flags individuais para cada ODS
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
        
        print(f"✅ Dados processados e salvos: {len(dados_json)} registros")
        
        # Calcular estatísticas dos ODS
        estatisticas = {}
        for ods in ['ODS 1', 'ODS 2', 'ODS 3', 'ODS 4', 'ODS 5', 'ODS 6', 'ODS 7', 'ODS 8', 'ODS 9', 'ODS 10', 'ODS 11', 'ODS 12', 'ODS 13', 'ODS 14', 'ODS 15', 'ODS 16', 'ODS 17', 'Geral']:
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
        
        return dados_json, estatisticas
        
    except Exception as e:
        print(f"❌ Erro ao processar dados: {e}")
        return None, None

if __name__ == "__main__":
    dados, stats = processar_dados_ods()
