#!/usr/bin/env python3
"""
Script para validar e gerar dados corretos dos ODS baseados na planilha Excel
"""

import pandas as pd
import json

def main():
    # Carregar dados da aba 'Análise de Conteúdo'
    df = pd.read_excel('Análise de Conteúdo - Luciano 22_06.xlsx', sheet_name='Análise de Conteúdo')
    
    print('=== VALIDAÇÃO DOS DADOS DOS ODS ===')
    print(f'Total de estudos: {len(df)}')
    print()
    
    # Analisar coluna O
    ods_column = df['ODS Mencionados pelos Autores'].fillna('')
    
    # Contar estudos que mencionam cada ODS
    ods_counts = {}
    ods_studies_count = {}
    
    for index, value in enumerate(ods_column):
        if value and str(value).strip():
            study_id = df.iloc[index]['ID'] if 'ID' in df.columns else index + 1
            # Dividir por vírgula ou ponto e vírgula
            ods_items = [item.strip() for item in str(value).replace(';', ',').split(',') if item.strip()]
            
            # Set para evitar contar o mesmo ODS múltiplas vezes no mesmo estudo
            unique_ods_in_study = set()
            
            for ods in ods_items:
                # Normalizar ODS
                if 'ODS' in ods.upper() or ods.isdigit():
                    # Extrair número do ODS
                    num = ''.join(filter(str.isdigit, ods))
                    if num:
                        normalized_ods = f'ODS {num}'
                    else:
                        normalized_ods = 'Geral'
                else:
                    normalized_ods = 'Geral'
                
                # Contar menções totais
                if normalized_ods not in ods_counts:
                    ods_counts[normalized_ods] = 0
                ods_counts[normalized_ods] += 1
                
                # Contar estudos únicos
                if normalized_ods not in unique_ods_in_study:
                    if normalized_ods not in ods_studies_count:
                        ods_studies_count[normalized_ods] = 0
                    ods_studies_count[normalized_ods] += 1
                    unique_ods_in_study.add(normalized_ods)
    
    # Validar dados atuais vs planilha
    print('=== DADOS CORRETOS DA PLANILHA ===')
    total_studies = len(df)
    
    # Todos os ODS de 1 a 17
    all_ods = [f'ODS {i}' for i in range(1, 18)]
    
    print('Estudos por ODS:')
    for ods in sorted(all_ods + ['Geral'], key=lambda x: (x != 'Geral', int(x.split()[-1]) if x != 'Geral' else 999)):
        count = ods_studies_count.get(ods, 0)
        percentage = (count / total_studies) * 100
        print(f'  {ods}: {count} estudos ({percentage:.1f}%)')
    
    print()
    print('=== ODS NÃO MENCIONADOS ===')
    not_mentioned = [ods for ods in all_ods if ods not in ods_studies_count]
    for ods in not_mentioned:
        print(f'  {ods}: 0 estudos (0.0%)')
    
    print()
    print('=== TOP 5 ODS MAIS MENCIONADOS ===')
    # Ordenar por número de estudos (excluindo Geral)
    ods_ranking = [(ods, count) for ods, count in ods_studies_count.items() if ods != 'Geral']
    ods_ranking.sort(key=lambda x: x[1], reverse=True)
    
    for i, (ods, count) in enumerate(ods_ranking[:5]):
        percentage = (count / total_studies) * 100
        print(f'  {i+1}. {ods}: {count} estudos ({percentage:.1f}%)')
    
    # Geral separadamente
    if 'Geral' in ods_studies_count:
        geral_count = ods_studies_count['Geral']
        geral_percentage = (geral_count / total_studies) * 100
        print(f'     Geral: {geral_count} estudos ({geral_percentage:.1f}%)')
    
    print()
    print('=== RESUMO PARA JAVASCRIPT ===')
    print(f'Total de estudos: {total_studies}')
    print(f'ODS únicos mencionados: {len([ods for ods in ods_studies_count.keys() if ods != "Geral"])}')
    print(f'Total de menções: {sum(ods_counts.values())}')
    print(f'Média de menções por estudo: {sum(ods_counts.values()) / total_studies:.1f}')
    
    # Gerar estrutura para JavaScript
    js_data = {}
    for ods in all_ods + ['Geral']:
        js_data[ods] = {
            'name': ods,
            'studiesCount': ods_studies_count.get(ods, 0),
            'totalMentions': ods_counts.get(ods, 0),
            'percentage': round((ods_studies_count.get(ods, 0) / total_studies) * 100, 1)
        }
    
    print()
    print('=== DADOS PARA JAVASCRIPT ===')
    print(json.dumps(js_data, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
