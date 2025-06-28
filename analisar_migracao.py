#!/usr/bin/env python3
"""
Script para migração de fonte de dados Excel
Compara estruturas e atualiza sistema para usar novo arquivo
"""

import pandas as pd
import json
import os
from datetime import datetime

def analisar_arquivo_excel(caminho_arquivo):
    """Analisar estrutura de um arquivo Excel"""
    try:
        print(f"📁 Analisando: {caminho_arquivo}")
        
        # Ler arquivo
        df = pd.read_excel(caminho_arquivo)
        
        # Informações básicas
        info = {
            "arquivo": caminho_arquivo,
            "existe": True,
            "linhas": len(df),
            "colunas": len(df.columns),
            "nomes_colunas": list(df.columns),
            "tipos_dados": df.dtypes.to_dict(),
            "primeira_linha": df.iloc[0].to_dict() if len(df) > 0 else {},
            "tamanho_mb": round(os.path.getsize(caminho_arquivo) / 1024 / 1024, 2)
        }
        
        print(f"  ✅ Linhas: {info['linhas']}")
        print(f"  ✅ Colunas: {info['colunas']}")
        print(f"  ✅ Tamanho: {info['tamanho_mb']} MB")
        
        return info, df
        
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return {
            "arquivo": caminho_arquivo,
            "existe": False,
            "erro": str(e)
        }, None

def comparar_estruturas(info_antigo, info_novo):
    """Comparar estruturas dos dois arquivos"""
    print("\n🔍 COMPARANDO ESTRUTURAS:")
    print("=" * 40)
    
    # Comparar número de linhas e colunas
    print(f"📊 Linhas: {info_antigo['linhas']} → {info_novo['linhas']} ({info_novo['linhas'] - info_antigo['linhas']:+d})")
    print(f"📊 Colunas: {info_antigo['colunas']} → {info_novo['colunas']} ({info_novo['colunas'] - info_antigo['colunas']:+d})")
    
    # Comparar nomes das colunas
    colunas_antigas = set(info_antigo['nomes_colunas'])
    colunas_novas = set(info_novo['nomes_colunas'])
    
    # Colunas removidas
    removidas = colunas_antigas - colunas_novas
    if removidas:
        print(f"\n❌ Colunas REMOVIDAS ({len(removidas)}):")
        for col in sorted(removidas):
            print(f"  - {col}")
    
    # Colunas adicionadas
    adicionadas = colunas_novas - colunas_antigas
    if adicionadas:
        print(f"\n✅ Colunas ADICIONADAS ({len(adicionadas)}):")
        for col in sorted(adicionadas):
            print(f"  + {col}")
    
    # Colunas mantidas
    mantidas = colunas_antigas & colunas_novas
    print(f"\n🔄 Colunas MANTIDAS ({len(mantidas)}):")
    for col in sorted(list(mantidas)[:10]):  # Mostrar apenas as primeiras 10
        print(f"  = {col}")
    if len(mantidas) > 10:
        print(f"  ... e mais {len(mantidas) - 10} colunas")
    
    return {
        "removidas": list(removidas),
        "adicionadas": list(adicionadas),
        "mantidas": list(mantidas),
        "compativel": len(removidas) == 0,  # Compatível se não removeu colunas essenciais
        "precisa_atualizacao": len(adicionadas) > 0 or len(removidas) > 0
    }

def verificar_colunas_essenciais(comparacao, colunas_essenciais):
    """Verificar se colunas essenciais foram mantidas"""
    print(f"\n🎯 VERIFICANDO COLUNAS ESSENCIAIS:")
    print("-" * 30)
    
    problemas = []
    for col in colunas_essenciais:
        if col in comparacao['removidas']:
            print(f"  ❌ CRÍTICO: '{col}' foi removida!")
            problemas.append(f"Coluna essencial '{col}' removida")
        elif col in comparacao['mantidas']:
            print(f"  ✅ OK: '{col}' mantida")
        else:
            print(f"  ⚠️  ATENÇÃO: '{col}' não encontrada em nenhum arquivo")
    
    return problemas

def gerar_plano_migracao(comparacao, problemas):
    """Gerar plano de migração baseado na análise"""
    print(f"\n📋 PLANO DE MIGRAÇÃO:")
    print("=" * 30)
    
    if problemas:
        print("🚨 PROBLEMAS CRÍTICOS ENCONTRADOS:")
        for problema in problemas:
            print(f"  - {problema}")
        print("\n❌ MIGRAÇÃO NÃO RECOMENDADA sem correções!")
        return False
    
    if not comparacao['precisa_atualizacao']:
        print("✅ Estruturas idênticas - migração simples")
        print("\nPLANO:")
        print("  1. Criar backup do arquivo atual")
        print("  2. Atualizar caminho nos scripts")
        print("  3. Regenerar dados JavaScript")
        print("  4. Testar visualização")
        return True
    
    if comparacao['compativel']:
        print("✅ Estruturas compatíveis - migração com atualizações")
        print("\nPLANO:")
        print("  1. Criar backup do arquivo atual")
        print("  2. Atualizar caminho nos scripts")
        if comparacao['adicionadas']:
            print("  3. Atualizar array 'columns' no HTML com novas colunas:")
            for col in comparacao['adicionadas']:
                print(f"     + '{col}'")
        print("  4. Regenerar dados JavaScript")
        print("  5. Testar visualização")
        print("  6. Verificar se novas colunas precisam formatação especial")
        return True
    
    print("⚠️ Migração complexa necessária")
    print("\nREQUER ANÁLISE MANUAL:")
    if comparacao['removidas']:
        print("  - Colunas removidas podem quebrar funcionalidades")
    print("  - Revisar todos os scripts antes da migração")
    return False

def criar_configuracao_migracao():
    """Criar arquivo de configuração para migração"""
    config = {
        "arquivo_atual": "Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx",
        "arquivo_novo": "Análise de Conteúdo - Luciano 22_06.xlsx",
        "timestamp_analise": datetime.now().isoformat(),
        "scripts_para_atualizar": [
            "processar_dados_ods.py",
            "gerar_tabela_abnt.py", 
            "gerar_tabela_apendice_abnt.py",
            "gerar_visualizacao_icones_ods.py"
        ],
        "backup_necessario": True,
        "regenerar_javascript": True
    }
    
    with open("config_migracao.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Configuração salva em: config_migracao.json")
    return config

def main():
    """Função principal"""
    print("🔄 ANÁLISE DE MIGRAÇÃO DE FONTE DE DADOS")
    print("=" * 50)
    
    # Definir caminhos
    arquivo_antigo = "Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx"
    arquivo_novo = "Análise de Conteúdo - Luciano 22_06.xlsx"
    
    # Colunas essenciais que não podem ser removidas
    colunas_essenciais = [
        "Link", "ID", "Autores", "Título", "Ano", 
        "ODS (Geral / Específico)", "Pilar CSC"
    ]
    
    # Analisar arquivos
    info_antigo, df_antigo = analisar_arquivo_excel(arquivo_antigo)
    info_novo, df_novo = analisar_arquivo_excel(arquivo_novo)
    
    if not info_antigo['existe'] or not info_novo['existe']:
        print("❌ Não é possível prosseguir - arquivo(s) não encontrado(s)")
        return
    
    # Comparar estruturas
    comparacao = comparar_estruturas(info_antigo, info_novo)
    
    # Verificar colunas essenciais
    problemas = verificar_colunas_essenciais(comparacao, colunas_essenciais)
    
    # Gerar plano
    migracao_ok = gerar_plano_migracao(comparacao, problemas)
    
    # Salvar análise completa
    relatorio = {
        "arquivo_antigo": info_antigo,
        "arquivo_novo": info_novo,
        "comparacao": comparacao,
        "problemas": problemas,
        "migracao_recomendada": migracao_ok,
        "timestamp": datetime.now().isoformat()
    }
    
    with open("relatorio_migracao.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
    
    # Criar configuração se migração for viável
    if migracao_ok:
        criar_configuracao_migracao()
        print(f"\n🚀 PRÓXIMOS PASSOS:")
        print("  1. Revisar o relatório: relatorio_migracao.json")
        print("  2. Executar migração: python executar_migracao.py")
    else:
        print(f"\n⚠️  AÇÃO NECESSÁRIA:")
        print("  1. Revisar problemas encontrados")
        print("  2. Corrigir arquivo ou ajustar scripts")
        print("  3. Executar análise novamente")
    
    print(f"\n📄 Relatório completo salvo em: relatorio_migracao.json")

if __name__ == "__main__":
    main()
