#!/usr/bin/env python3
"""
Script de validação final da migração de dados ODS/CSC
Compara estatísticas entre arquivo antigo e novo para validar integridade
"""

import pandas as pd
import json
import re
import os
from datetime import datetime

def validar_migracao():
    print("🔍 VALIDAÇÃO FINAL DA MIGRAÇÃO")
    print("=" * 50)
    
    arquivo_antigo = 'Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx'
    arquivo_novo = 'Análise de Conteúdo - Luciano 22_06.xlsx'
    
    resultados = {
        'timestamp': datetime.now().isoformat(),
        'arquivos_comparados': {
            'antigo': arquivo_antigo,
            'novo': arquivo_novo
        },
        'validacao_aprovada': True,
        'problemas_encontrados': [],
        'comparacao_estatisticas': {}
    }
    
    def processar_arquivo(arquivo, nome):
        print(f"\n📊 Processando {nome}: {arquivo}")
        
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            return None
        
        try:
            df = pd.read_excel(arquivo)
            print(f"✅ Carregado: {len(df)} registros, {len(df.columns)} colunas")
            
            # Mapeamento de colunas
            ods_coluna = 'ODS (Geral / Específico)' if 'ODS (Geral / Específico)' in df.columns else 'ODS Mencionados pelos Autores'
            
            if ods_coluna not in df.columns:
                print(f"❌ Coluna ODS não encontrada em {arquivo}")
                return None
            
            # Calcular estatísticas ODS
            estatisticas = {}
            ods_list = ['ODS 1', 'ODS 2', 'ODS 3', 'ODS 4', 'ODS 5', 'ODS 6', 'ODS 7', 'ODS 8', 'ODS 9', 'ODS 10', 'ODS 11', 'ODS 12', 'ODS 13', 'ODS 14', 'ODS 15', 'ODS 16', 'ODS 17', 'Geral']
            
            for ods in ods_list:
                count = 0
                for index, row in df.iterrows():
                    ods_valor = str(row.get(ods_coluna, ''))
                    if re.search(r'\b' + re.escape(ods) + r'\b', ods_valor):
                        count += 1
                
                percentage = (count / len(df)) * 100 if len(df) > 0 else 0
                estatisticas[ods] = {
                    'count': count,
                    'percentage': round(percentage, 1)
                }
            
            dados = {
                'arquivo': arquivo,
                'registros': len(df),
                'colunas': len(df.columns),
                'coluna_ods_usada': ods_coluna,
                'estatisticas': estatisticas
            }
            
            return dados
            
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")
            return None
    
    # Processar ambos os arquivos
    dados_antigo = processar_arquivo(arquivo_antigo, "ARQUIVO ANTIGO")
    dados_novo = processar_arquivo(arquivo_novo, "ARQUIVO NOVO")
    
    if not dados_antigo or not dados_novo:
        print("❌ Falha na validação: não foi possível processar ambos os arquivos")
        resultados['validacao_aprovada'] = False
        resultados['problemas_encontrados'].append("Falha no processamento de arquivos")
        return resultados
    
    # Comparar estatísticas
    print(f"\n🔄 COMPARAÇÃO DE RESULTADOS:")
    print("-" * 70)
    print(f"{'ODS':<10} {'ANTIGO':<15} {'NOVO':<15} {'DIFERENÇA':<15} {'STATUS'}")
    print("-" * 70)
    
    diferencas_criticas = 0
    ods_list = ['ODS 1', 'ODS 2', 'ODS 3', 'ODS 4', 'ODS 5', 'ODS 6', 'ODS 7', 'ODS 8', 'ODS 9', 'ODS 10', 'ODS 11', 'ODS 12', 'ODS 13', 'ODS 14', 'ODS 15', 'ODS 16', 'ODS 17', 'Geral']
    
    for ods in ods_list:
        antigo_count = dados_antigo['estatisticas'][ods]['count']
        novo_count = dados_novo['estatisticas'][ods]['count']
        diferenca = novo_count - antigo_count
        
        if diferenca == 0:
            status = "✅ IGUAL"
        elif abs(diferenca) <= 1:
            status = "⚠️  PEQUENA"
        else:
            status = "❌ CRÍTICA"
            diferencas_criticas += 1
            resultados['problemas_encontrados'].append(f"Diferença crítica em {ods}: {antigo_count} → {novo_count}")
        
        resultados['comparacao_estatisticas'][ods] = {
            'antigo': antigo_count,
            'novo': novo_count,
            'diferenca': diferenca,
            'status': status.replace('✅ ', '').replace('⚠️  ', '').replace('❌ ', '')
        }
        
        print(f"{ods:<10} {antigo_count:>3} ({dados_antigo['estatisticas'][ods]['percentage']:>4.1f}%){novo_count:>7} ({dados_novo['estatisticas'][ods]['percentage']:>4.1f}%){diferenca:>8}{status:>15}")
    
    # Validação final
    print("\n" + "=" * 70)
    
    if diferencas_criticas > 0:
        print(f"❌ VALIDAÇÃO REPROVADA: {diferencas_criticas} diferenças críticas encontradas")
        resultados['validacao_aprovada'] = False
    else:
        print("✅ VALIDAÇÃO APROVADA: Migração bem-sucedida!")
        print("🎯 Os dados foram migrados corretamente.")
        print("📊 Todas as estatísticas ODS estão consistentes.")
    
    # Salvar relatório
    with open('validacao_migracao_final.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print(f"\n📋 Relatório completo salvo em: validacao_migracao_final.json")
    
    return resultados

if __name__ == "__main__":
    resultado = validar_migracao()
