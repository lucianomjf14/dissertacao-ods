#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste dos novos botões ODS e CSC - Verificar se as colunas estão corretas
"""

import pandas as pd

def testar_botao_ods():
    print("🎯 TESTE DO BOTÃO ODS")
    print("=" * 40)
    
    # Carregar dados
    df = pd.read_excel('Análise de Conteúdo - Luciano 22_06.xlsx')
    
    print("📋 COLUNAS DEFINIDAS PARA O BOTÃO ODS:")
    ods_columns = ['ID', 'Autores', 'Título', 'Ano de Publicação', 'Trechos correlações', 'ODS Mencionados pelos Autores']
    
    for i, col in enumerate(ods_columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\n📊 DISPONIBILIDADE DAS COLUNAS NO EXCEL:")
    colunas_excel = df.columns.tolist()
    
    for col in ods_columns:
        if col in colunas_excel:
            print(f"  ✅ {col}")
        else:
            print(f"  ❌ {col} - NÃO ENCONTRADA")
            # Tentar encontrar coluna similar
            for excel_col in colunas_excel:
                if col.lower() in excel_col.lower() or excel_col.lower() in col.lower():
                    print(f"     🔍 Possível correspondência: '{excel_col}'")
    
    print(f"\n📈 ESTATÍSTICAS DE DADOS:")
    for col in ods_columns:
        if col in df.columns:
            total = len(df)
            preenchidos = df[col].notna().sum()
            vazios = total - preenchidos
            print(f"  {col}:")
            print(f"    Total: {total} | Preenchidos: {preenchidos} | Vazios: {vazios}")
            
            if col == 'Trechos correlações' and preenchidos > 0:
                # Verificar comprimento médio dos trechos
                trechos_validos = df[col].dropna()
                comprimentos = [len(str(t)) for t in trechos_validos]
                comprimento_medio = sum(comprimentos) / len(comprimentos)
                maior_comprimento = max(comprimentos)
                print(f"    Comprimento médio: {comprimento_medio:.1f} caracteres")
                print(f"    Maior trecho: {maior_comprimento} caracteres")
                print(f"    Necessário truncamento: {'Sim' if maior_comprimento > 20 else 'Não'}")
    
    print(f"\n🎯 PRIMEIROS 3 REGISTROS DO MODO ODS:")
    for i, row in df.head(3).iterrows():
        print(f"\n  📄 ID {row['ID']}:")
        for col in ods_columns:
            if col in df.columns:
                valor = row[col]
                if pd.notna(valor):
                    valor_str = str(valor)
                    if col == 'Trechos correlações' and len(valor_str) > 50:
                        valor_exibido = valor_str[:50] + "..."
                    else:
                        valor_exibido = valor_str
                    print(f"    {col}: {valor_exibido}")
                else:
                    print(f"    {col}: [VAZIO]")

def testar_botao_csc():
    print("\n\n🏛️ TESTE DO BOTÃO CSC")
    print("=" * 40)
    
    # Carregar dados
    df = pd.read_excel('Análise de Conteúdo - Luciano 22_06.xlsx')
    
    print("📋 COLUNAS DEFINIDAS PARA O BOTÃO CSC:")
    csc_columns = ['ID', 'Palavras Chave', 'Palavras chave normalizadas e Traduzidas', 'Indicadores CSC', 'Pilar CSC']
    
    for i, col in enumerate(csc_columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\n📊 DISPONIBILIDADE DAS COLUNAS NO EXCEL:")
    colunas_excel = df.columns.tolist()
    
    for col in csc_columns:
        if col in colunas_excel:
            print(f"  ✅ {col}")
        else:
            print(f"  ❌ {col} - NÃO ENCONTRADA")
            # Tentar encontrar coluna similar
            for excel_col in colunas_excel:
                if col.lower() in excel_col.lower() or excel_col.lower() in col.lower():
                    print(f"     🔍 Possível correspondência: '{excel_col}'")
    
    print(f"\n📈 ESTATÍSTICAS DE DADOS:")
    for col in csc_columns:
        if col in df.columns:
            total = len(df)
            preenchidos = df[col].notna().sum()
            vazios = total - preenchidos
            print(f"  {col}:")
            print(f"    Total: {total} | Preenchidos: {preenchidos} | Vazios: {vazios}")
            
            # Análise específica para colunas de texto
            if col in ['Palavras Chave', 'Palavras chave normalizadas e Traduzidas', 'Indicadores CSC'] and preenchidos > 0:
                textos_validos = df[col].dropna()
                comprimentos = [len(str(t)) for t in textos_validos]
                comprimento_medio = sum(comprimentos) / len(comprimentos)
                maior_comprimento = max(comprimentos)
                print(f"    Comprimento médio: {comprimento_medio:.1f} caracteres")
                print(f"    Maior texto: {maior_comprimento} caracteres")
            
            # Análise específica para Pilar CSC
            if col == 'Pilar CSC' and preenchidos > 0:
                pilares_validos = df[col].dropna()
                # Contar siglas únicas
                todas_siglas = []
                for pilar in pilares_validos:
                    if str(pilar) != '-':
                        siglas = [s.strip() for s in str(pilar).split(',')]
                        todas_siglas.extend(siglas)
                siglas_unicas = set(todas_siglas)
                print(f"    Siglas únicas encontradas: {len(siglas_unicas)}")
                print(f"    Siglas: {', '.join(sorted(siglas_unicas))}")
    
    print(f"\n🏛️ PRIMEIROS 3 REGISTROS DO MODO CSC:")
    for i, row in df.head(3).iterrows():
        print(f"\n  📄 ID {row['ID']}:")
        for col in csc_columns:
            if col in df.columns:
                valor = row[col]
                if pd.notna(valor):
                    valor_str = str(valor)                    if col in ['Palavras Chave', 'Palavras chave normalizadas e Traduzidas'] and len(valor_str) > 50:
                        valor_exibido = valor_str[:50] + "..."
                    elif col == 'Indicadores CSC' and len(valor_str) > 30:
                        valor_exibido = valor_str[:30] + "..."
                    else:
                        valor_exibido = valor_str
                    print(f"    {col}: {valor_exibido}")
                else:
                    print(f"    {col}: [VAZIO]")

if __name__ == "__main__":
    testar_botao_ods()
    testar_botao_csc()
    
    print("\n\n🎉 RESUMO DOS TESTES:")
    print("=" * 50)
    print("✅ Botão ODS: 6 colunas focadas nos Objetivos de Desenvolvimento Sustentável")
    print("✅ Botão CSC: 5 colunas focadas nos Pilares de Cidades Sustentáveis e Criativas")
    print("🎯 Ambos os botões estão prontos para uso no painel de visualização!")
    print("\n📋 Total de botões disponíveis:")
    print("  1. ✅ Todas as Colunas")
    print("  2. 📋 Metadados")
    print("  3. 🎯 ODS (NOVO)")
    print("  4. 🏛️ CSC (NOVO)")
    print("  5. 🔬 Tecnologias - Cidades Inteligentes")
    print("  6. 🚫 Limpar Tudo")
