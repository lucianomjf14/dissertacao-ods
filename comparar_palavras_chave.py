#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise Comparativa: Palavras-Chave Originais vs Normalizadas e Traduzidas
Compara as duas colunas de palavras-chave para identificar diferenças e padrões
"""

import pandas as pd
import json
from collections import Counter

def comparar_palavras_chave():
    """
    Comparação detalhada entre as duas colunas de palavras-chave
    """
    print("🔍 ANÁLISE COMPARATIVA: PALAVRAS-CHAVE ORIGINAIS vs NORMALIZADAS")
    print("=" * 80)
    
    # Carregar dados das análises anteriores
    try:
        with open('analise_palavras_chave.json', 'r', encoding='utf-8') as f:
            dados_originais = json.load(f)
        
        with open('analise_palavras_chave_normalizadas.json', 'r', encoding='utf-8') as f:
            dados_normalizados = json.load(f)
        
        print("✅ Dados carregados com sucesso!")
    except FileNotFoundError as e:
        print(f"❌ Erro: Arquivo não encontrado - {e}")
        return
    
    # Estatísticas comparativas
    print(f"\n📊 COMPARAÇÃO ESTATÍSTICA:")
    print(f"{'Métrica':<40} {'Original':<15} {'Normalizada':<15} {'Diferença':<15}")
    print("-" * 85)
    
    total_palavras_orig = dados_originais['analise_termos']['total_palavras']
    total_palavras_norm = dados_normalizados['analise_termos']['total_palavras']
    diff_total = total_palavras_norm - total_palavras_orig
    
    termos_unicos_orig = dados_originais['analise_termos']['termos_unicos']
    termos_unicos_norm = dados_normalizados['analise_termos']['termos_unicos']
    diff_unicos = termos_unicos_norm - termos_unicos_orig
    
    media_orig = dados_originais['analise_termos']['media_palavras_por_registro']
    media_norm = dados_normalizados['analise_termos']['media_palavras_por_registro']
    diff_media = media_norm - media_orig
    
    print(f"{'Total de palavras':<40} {total_palavras_orig:<15} {total_palavras_norm:<15} {diff_total:+d}")
    print(f"{'Termos únicos':<40} {termos_unicos_orig:<15} {termos_unicos_norm:<15} {diff_unicos:+d}")
    print(f"{'Média por registro':<40} {media_orig:<15.1f} {media_norm:<15.1f} {diff_media:+.1f}")
    
    # Análise de eficiência da normalização
    print(f"\n🎯 EFICIÊNCIA DA NORMALIZAÇÃO:")
    reducao_percentual = (abs(diff_unicos) / termos_unicos_orig) * 100
    print(f"• Redução de termos únicos: {abs(diff_unicos)} termos ({reducao_percentual:.1f}%)")
    print(f"• Consolidação de vocabulário: {'✅ Eficaz' if diff_unicos < 0 else '❌ Ineficaz'}")
    
    # Carregar listas completas de termos
    df_orig = pd.read_csv('termos_palavras_chave.csv')
    df_norm = pd.read_csv('termos_palavras_chave_normalizadas.csv')
    
    termos_orig_set = set(df_orig['termo'].str.lower())
    termos_norm_set = set(df_norm['termo'].str.lower())
    
    # Análise de sobreposição
    termos_comuns = termos_orig_set.intersection(termos_norm_set)
    termos_apenas_orig = termos_orig_set - termos_norm_set
    termos_apenas_norm = termos_norm_set - termos_orig_set
    
    print(f"\n🔄 ANÁLISE DE SOBREPOSIÇÃO:")
    print(f"• Termos comuns: {len(termos_comuns)}")
    print(f"• Apenas na original: {len(termos_apenas_orig)}")
    print(f"• Apenas na normalizada: {len(termos_apenas_norm)}")
    print(f"• Taxa de sobreposição: {(len(termos_comuns)/max(len(termos_orig_set), len(termos_norm_set)))*100:.1f}%")
    
    # Top 10 termos mais frequentes - comparação
    print(f"\n🏆 COMPARAÇÃO DOS TOP 10 TERMOS:")
    print(f"{'Posição':<10} {'Original':<35} {'Freq':<8} {'Normalizada':<35} {'Freq':<8}")
    print("-" * 96)
    
    top_orig = list(dados_originais['top_20_termos'].items())[:10]
    top_norm = list(dados_normalizados['top_20_termos'].items())[:10]
    
    for i in range(10):
        pos = i + 1
        termo_orig, freq_orig = top_orig[i] if i < len(top_orig) else ("", 0)
        termo_norm, freq_norm = top_norm[i] if i < len(top_norm) else ("", 0)
        print(f"{pos:<10} {termo_orig:<35} {freq_orig:<8} {termo_norm:<35} {freq_norm:<8}")
    
    # Análise de traduções/normalizações mais significativas
    print(f"\n🔄 EXEMPLOS DE NORMALIZAÇÃO/TRADUÇÃO:")
    
    # Mapeamento manual de alguns termos conhecidos
    mapeamentos_esperados = {
        'smart cities': 'cidades inteligentes',
        'smart city': 'cidades inteligentes',
        'sustainable development': 'desenvolvimento sustentável',
        'artificial intelligence': 'inteligência artificial',
        'internet of things': 'iot',
        'digital twins': 'gêmeos digitais',
        'climate change': 'mudanças climáticas',
        'sustainable cities': 'cidades sustentáveis'
    }
    
    print("• Principais traduções identificadas:")
    for orig, norm in mapeamentos_esperados.items():
        if orig in df_orig['termo'].str.lower().values and norm in df_norm['termo'].str.lower().values:
            freq_orig = df_orig[df_orig['termo'].str.lower() == orig]['frequencia'].iloc[0] if len(df_orig[df_orig['termo'].str.lower() == orig]) > 0 else 0
            freq_norm = df_norm[df_norm['termo'].str.lower() == norm]['frequencia'].iloc[0] if len(df_norm[df_norm['termo'].str.lower() == norm]) > 0 else 0
            print(f"  - '{orig}' ({freq_orig}x) → '{norm}' ({freq_norm}x)")
    
    # Análise de idioma
    print(f"\n🌐 ANÁLISE DE IDIOMA:")
    
    # Contar termos em inglês vs português (heurística)
    termos_ingles_orig = sum(1 for termo in df_orig['termo'] if any(palavra in termo.lower() for palavra in ['smart', 'city', 'cities', 'sustainable', 'development', 'internet', 'things', 'intelligence', 'data', 'digital', 'climate', 'change']))
    termos_ingles_norm = sum(1 for termo in df_norm['termo'] if any(palavra in termo.lower() for palavra in ['smart', 'city', 'cities', 'sustainable', 'development', 'internet', 'things', 'intelligence', 'data', 'digital', 'climate', 'change']))
    
    print(f"• Termos em inglês (estimado):")
    print(f"  - Original: {termos_ingles_orig} ({(termos_ingles_orig/termos_unicos_orig)*100:.1f}%)")
    print(f"  - Normalizada: {termos_ingles_norm} ({(termos_ingles_norm/termos_unicos_norm)*100:.1f}%)")
    
    # Salvar relatório comparativo
    relatorio = {
        'resumo_comparativo': {
            'total_palavras': {
                'original': total_palavras_orig,
                'normalizada': total_palavras_norm,
                'diferenca': diff_total
            },
            'termos_unicos': {
                'original': termos_unicos_orig,
                'normalizada': termos_unicos_norm,
                'diferenca': diff_unicos,
                'reducao_percentual': round(reducao_percentual, 1)
            },
            'sobreposicao': {
                'termos_comuns': len(termos_comuns),
                'apenas_original': len(termos_apenas_orig),
                'apenas_normalizada': len(termos_apenas_norm),
                'taxa_sobreposicao': round((len(termos_comuns)/max(len(termos_orig_set), len(termos_norm_set)))*100, 1)
            }
        },
        'eficiencia_normalizacao': {
            'consolidacao_eficaz': diff_unicos < 0,
            'termos_eliminados': abs(diff_unicos) if diff_unicos < 0 else 0,
            'avaliacao': 'Eficaz' if diff_unicos < 0 else 'Ineficaz'
        }
    }
    
    with open('relatorio_comparativo_palavras_chave.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Relatório comparativo salvo em 'relatorio_comparativo_palavras_chave.json'")
    
    return relatorio

if __name__ == "__main__":
    relatorio = comparar_palavras_chave()
