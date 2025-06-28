#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise Detalhada das Discrepâncias
Investigação aprofundada das diferenças encontradas
"""

import pandas as pd
import json
from collections import Counter
import re

def analise_detalhada_ods():
    """Análise detalhada dos dados dos ODS para entender as discrepâncias"""
    
    print("🔍 ANÁLISE DETALHADA DAS DISCREPÂNCIAS DOS ODS")
    print("="*60)
    
    try:
        df = pd.read_excel("Análise de Conteúdo - Luciano 22_06.xlsx")
        
        # Verificar conteúdo da coluna ODS
        coluna_ods = 'ODS Mencionados pelos Autores'
        dados_ods = df[coluna_ods].fillna('').astype(str)
        
        print(f"\n📋 ANÁLISE DA COLUNA: {coluna_ods}")
        print(f"📊 Total de registros: {len(dados_ods)}")
        
        # Mostrar alguns exemplos dos dados
        print(f"\n📝 AMOSTRA DOS DADOS (primeiros 10 registros):")
        for i, valor in enumerate(dados_ods.head(10)):
            print(f"   {i+1:2d}. {valor}")
        
        # Análise de padrões
        print(f"\n🔍 ANÁLISE DE PADRÕES:")
        
        # Contadores detalhados
        contadores = {}
        registros_detalhados = {}
        
        for i, valor in enumerate(dados_ods):
            registro_num = i + 1
            valor_limpo = valor.strip().lower()
            
            # ODS 1
            if 'ods 1' in valor_limpo or 'ods1' in valor_limpo:
                contadores.setdefault('ODS 1', []).append(registro_num)
            
            # ODS 7
            if 'ods 7' in valor_limpo or 'ods7' in valor_limpo:
                contadores.setdefault('ODS 7', []).append(registro_num)
            
            # ODS 9
            if 'ods 9' in valor_limpo or 'ods9' in valor_limpo:
                contadores.setdefault('ODS 9', []).append(registro_num)
            
            # ODS 11
            if 'ods 11' in valor_limpo or 'ods11' in valor_limpo:
                contadores.setdefault('ODS 11', []).append(registro_num)
            
            # ODS 13
            if 'ods 13' in valor_limpo or 'ods13' in valor_limpo:
                contadores.setdefault('ODS 13', []).append(registro_num)
            
            # ODS 14
            if 'ods 14' in valor_limpo or 'ods14' in valor_limpo:
                contadores.setdefault('ODS 14', []).append(registro_num)
            
            # ODS 5
            if 'ods 5' in valor_limpo or 'ods5' in valor_limpo:
                contadores.setdefault('ODS 5', []).append(registro_num)
            
            # Referências gerais
            if ('geral' in valor_limpo or 'agenda 2030' in valor_limpo or 
                'objetivos de desenvolvimento sustentável' in valor_limpo) and not any(f'ods {i}' in valor_limpo for i in range(1, 18)):
                contadores.setdefault('Referências Gerais', []).append(registro_num)
        
        # Mostrar resultados detalhados
        print(f"\n📊 CONTAGENS DETALHADAS:")
        for ods, registros in contadores.items():
            print(f"   {ods}: {len(registros)} ocorrências")
            print(f"      Registros: {registros[:10]}{'...' if len(registros) > 10 else ''}")
        
        # Verificar registros vazios ou problemáticos
        vazios = sum(1 for valor in dados_ods if not valor.strip() or valor.lower() == 'nan')
        print(f"\n⚠️ Registros vazios/nulos: {vazios}")
        
        # Análise de conteúdo único
        valores_unicos = dados_ods.value_counts()
        print(f"\n📈 VALORES MAIS FREQUENTES:")
        for valor, freq in valores_unicos.head(10).items():
            if valor.strip() and valor.lower() != 'nan':
                print(f"   '{valor}': {freq} ocorrências")
        
        # Salvar análise detalhada
        analise = {
            "total_registros": len(dados_ods),
            "contagens_por_ods": {ods: len(registros) for ods, registros in contadores.items()},
            "registros_por_ods": contadores,
            "registros_vazios": vazios,
            "valores_unicos": valores_unicos.head(20).to_dict()
        }
        
        with open("analise_detalhada_ods.json", "w", encoding="utf-8") as f:
            json.dump(analise, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Análise detalhada salva em: analise_detalhada_ods.json")
        
        return analise
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        return None

def analise_palavras_chave():
    """Análise das colunas de palavras-chave para tecnologias"""
    
    print(f"\n🔍 ANÁLISE DETALHADA DAS TECNOLOGIAS")
    print("="*60)
    
    try:
        df = pd.read_excel("Análise de Conteúdo - Luciano 22_06.xlsx")
        
        # Colunas de interesse
        colunas_tech = ['Palavras Chave', 'Palavras chave normalizadas e Traduzidas', 
                       'Aspecto Principal - Estudo', 'Categorias']
        
        tecnologias_busca = {
            'IoT': ['iot', 'internet of things', 'internet das coisas', 'sensores'],
            'IA': ['inteligência artificial', 'artificial intelligence', 'machine learning', 'ai', 'deep learning'],
            'Big Data': ['big data', 'dados massivos', 'data analytics'],
            'Gêmeos Digitais': ['digital twin', 'gêmeo digital', 'digital twins', 'twins'],
            'Metaverso': ['metaverse', 'metaverso', 'virtual reality', 'realidade virtual'],
            'Impressão 3D': ['3d printing', 'impressão 3d', 'fabricação digital', 'additive manufacturing']
        }
        
        for coluna in colunas_tech:
            if coluna in df.columns:
                print(f"\n📋 ANÁLISE DA COLUNA: {coluna}")
                dados = df[coluna].fillna('').astype(str)
                
                for tech, termos in tecnologias_busca.items():
                    registros_encontrados = []
                    for i, valor in enumerate(dados):
                        if any(termo in valor.lower() for termo in termos):
                            registros_encontrados.append(i + 1)
                    
                    print(f"   🔬 {tech}: {len(registros_encontrados)} ocorrências")
                    if registros_encontrados:
                        print(f"      Registros: {registros_encontrados[:5]}{'...' if len(registros_encontrados) > 5 else ''}")
                
        # Análise consolidada
        print(f"\n📊 ANÁLISE CONSOLIDADA (todas as colunas):")
        resultados_consolidados = {}
        
        for tech, termos in tecnologias_busca.items():
            registros_unicos = set()
            for coluna in colunas_tech:
                if coluna in df.columns:
                    dados = df[coluna].fillna('').astype(str)
                    for i, valor in enumerate(dados):
                        if any(termo in valor.lower() for termo in termos):
                            registros_unicos.add(i + 1)
            
            resultados_consolidados[tech] = list(registros_unicos)
            print(f"   🎯 {tech}: {len(registros_unicos)} estudos únicos")
        
        # Salvar resultados
        with open("analise_tecnologias_detalhada.json", "w", encoding="utf-8") as f:
            json.dump(resultados_consolidados, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Análise de tecnologias salva em: analise_tecnologias_detalhada.json")
        
        return resultados_consolidados
        
    except Exception as e:
        print(f"❌ Erro na análise de tecnologias: {e}")
        return None

def investigar_discrepancia_ods1():
    """Investigação específica da grande discrepância do ODS 1"""
    
    print(f"\n🚨 INVESTIGAÇÃO ESPECÍFICA - ODS 1")
    print("="*60)
    
    try:
        df = pd.read_excel("Análise de Conteúdo - Luciano 22_06.xlsx")
        
        coluna_ods = 'ODS Mencionados pelos Autores'
        dados_ods = df[coluna_ods].fillna('').astype(str)
        
        print(f"📋 Buscando menções do ODS 1...")
        
        registros_ods1 = []
        for i, valor in enumerate(dados_ods):
            valor_limpo = valor.strip().lower()
            if 'ods 1' in valor_limpo or 'ods1' in valor_limpo:
                registros_ods1.append({
                    'registro': i + 1,
                    'valor_original': valor,
                    'id': df.iloc[i]['ID'] if 'ID' in df.columns else i+1
                })
        
        print(f"🔍 Encontrados {len(registros_ods1)} registros com ODS 1:")
        for reg in registros_ods1[:10]:  # Mostrar apenas os primeiros 10
            print(f"   Registro {reg['registro']} (ID: {reg['id']}): '{reg['valor_original']}'")
        
        if len(registros_ods1) > 10:
            print(f"   ... e mais {len(registros_ods1) - 10} registros")
        
        # Verificar se há algum padrão que explique a discrepância
        # Talvez esteja contando algo diferente do que deveria
        
        print(f"\n🤔 POSSÍVEIS EXPLICAÇÕES PARA A DISCREPÂNCIA:")
        print(f"   • Documento original pode ter usado critérios diferentes")
        print(f"   • Pode ter havido confusão entre 'ODS 1' e outras categorias")
        print(f"   • Dados podem ter sido atualizados após a redação do documento")
        print(f"   • Método de contagem pode ter sido diferente")
        
        return registros_ods1
        
    except Exception as e:
        print(f"❌ Erro na investigação do ODS 1: {e}")
        return None

def main():
    """Função principal da análise detalhada"""
    
    print("🔍 ANÁLISE DETALHADA DAS DISCREPÂNCIAS")
    print("="*80)
    
    # Análise detalhada dos ODS
    analise_ods = analise_detalhada_ods()
    
    # Análise detalhada das tecnologias
    analise_tech = analise_palavras_chave()
    
    # Investigação específica do ODS 1
    investigacao_ods1 = investigar_discrepancia_ods1()
    
    print(f"\n✅ ANÁLISE DETALHADA CONCLUÍDA")
    print(f"📁 Arquivos gerados:")
    print(f"   • analise_detalhada_ods.json")
    print(f"   • analise_tecnologias_detalhada.json")

if __name__ == "__main__":
    main()
