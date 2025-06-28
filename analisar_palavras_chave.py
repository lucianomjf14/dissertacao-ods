#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise de Palavras-Chave - Termos Únicos
Analisa a coluna 'Palavras Chave' para contar termos únicos
"""

import pandas as pd
import re
from collections import Counter
import json

def limpar_e_separar_palavras(texto):
    """
    Limpa o texto e separa as palavras-chave
    """
    if pd.isna(texto) or texto == '':
        return []
    
    # Converter para string e limpar
    texto = str(texto).strip()
    
    # Separar por vírgulas, ponto-e-vírgula, ou outras separações comuns
    # Padrões comuns: vírgula, ponto-e-vírgula, quebra de linha
    separadores = r'[,;|\n\r]+'
    palavras = re.split(separadores, texto)
    
    # Limpar cada palavra
    palavras_limpas = []
    for palavra in palavras:
        # Remover espaços, aspas, parênteses
        palavra_limpa = re.sub(r'["\'\(\)\[\]{}]', '', palavra.strip())
        palavra_limpa = palavra_limpa.strip()
        
        # Ignorar palavras muito curtas ou vazias
        if len(palavra_limpa) > 2:
            palavras_limpas.append(palavra_limpa.lower())
    
    return palavras_limpas

def analisar_palavras_chave():
    """
    Análise principal das palavras-chave
    """
    print("🔍 Iniciando análise de palavras-chave...")
    
    # Carregar dados
    try:
        df = pd.read_excel('Análise de Conteúdo - Luciano 22_06.xlsx')
        print(f"✅ Arquivo carregado com sucesso: {len(df)} registros")
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")
        return
    
    # Verificar se a coluna existe
    if 'Palavras Chave' not in df.columns:
        print("❌ Coluna 'Palavras Chave' não encontrada!")
        print("Colunas disponíveis:", list(df.columns))
        return
    
    print(f"📊 Analisando coluna 'Palavras Chave'...")
    
    # Estatísticas básicas
    total_registros = len(df)
    registros_com_palavras = df['Palavras Chave'].notna().sum()
    registros_vazios = total_registros - registros_com_palavras
    
    print(f"\n📈 ESTATÍSTICAS BÁSICAS:")
    print(f"• Total de registros: {total_registros}")
    print(f"• Registros com palavras-chave: {registros_com_palavras}")
    print(f"• Registros vazios/nulos: {registros_vazios}")
    print(f"• Percentual preenchido: {(registros_com_palavras/total_registros)*100:.1f}%")
    
    # Processar todas as palavras-chave
    todas_palavras = []
    registros_processados = 0
    
    for idx, valor in df['Palavras Chave'].items():
        palavras = limpar_e_separar_palavras(valor)
        todas_palavras.extend(palavras)
        if palavras:
            registros_processados += 1
    
    # Contar termos únicos
    contador_palavras = Counter(todas_palavras)
    termos_unicos = len(contador_palavras)
    total_palavras = len(todas_palavras)
    
    print(f"\n🔤 ANÁLISE DE TERMOS:")
    print(f"• Total de palavras encontradas: {total_palavras}")
    print(f"• Termos únicos: {termos_unicos}")
    print(f"• Média de palavras por registro: {total_palavras/registros_processados:.1f}")
    
    # Top 20 termos mais frequentes
    print(f"\n🏆 TOP 20 TERMOS MAIS FREQUENTES:")
    for i, (termo, freq) in enumerate(contador_palavras.most_common(20), 1):
        print(f"{i:2}. {termo:<30} ({freq} vezes)")
    
    # Análise de distribuição
    print(f"\n📊 DISTRIBUIÇÃO DE FREQUÊNCIA:")
    freq_distribuicao = Counter(contador_palavras.values())
    for freq, qtd in sorted(freq_distribuicao.items(), reverse=True)[:10]:
        print(f"• {qtd} termos aparecem {freq} vez(es)")
    
    # Termos que aparecem apenas uma vez (hapax legomena)
    termos_unicos_freq = sum(1 for freq in contador_palavras.values() if freq == 1)
    print(f"• Termos que aparecem apenas 1 vez: {termos_unicos_freq} ({(termos_unicos_freq/termos_unicos)*100:.1f}%)")
      # Salvar resultados detalhados
    resultados = {
        'estatisticas_basicas': {
            'total_registros': int(total_registros),
            'registros_com_palavras': int(registros_com_palavras),
            'registros_vazios': int(registros_vazios),
            'percentual_preenchido': round((registros_com_palavras/total_registros)*100, 1)
        },
        'analise_termos': {
            'total_palavras': int(total_palavras),
            'termos_unicos': int(termos_unicos),
            'media_palavras_por_registro': round(total_palavras/registros_processados, 1)
        },
        'top_20_termos': {termo: int(freq) for termo, freq in contador_palavras.most_common(20)},
        'distribuicao_frequencia': {int(k): int(v) for k, v in freq_distribuicao.items()},
        'termos_unicos_freq': int(termos_unicos_freq)
    }
    
    # Salvar em JSON
    with open('analise_palavras_chave.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultados salvos em 'analise_palavras_chave.json'")
    
    # Salvar lista completa de termos em CSV
    df_termos = pd.DataFrame([
        {'termo': termo, 'frequencia': freq}
        for termo, freq in contador_palavras.most_common()
    ])
    df_termos.to_csv('termos_palavras_chave.csv', index=False, encoding='utf-8')
    print(f"📄 Lista completa salva em 'termos_palavras_chave.csv'")
    
    return resultados

if __name__ == "__main__":
    resultados = analisar_palavras_chave()
