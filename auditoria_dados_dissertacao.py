#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoria de Dados da Dissertação
Verificação criteriosa entre o documento de resultados e os dados da planilha
"""

import pandas as pd
import json
from collections import Counter
import re

def extrair_dados_planilha():
    """Carrega e processa os dados da planilha"""
    try:
        # Carregar a planilha
        df = pd.read_excel("Análise de Conteúdo - Luciano 22_06.xlsx")
        
        print(f"✅ Planilha carregada com sucesso")
        print(f"📊 Total de linhas: {len(df)}")
        print(f"📋 Total de colunas: {len(df.columns)}")
        print(f"📝 Colunas disponíveis: {list(df.columns)}")
        
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar planilha: {e}")
        return None

def verificar_informacoes_quantitativas(df):
    """Verifica todas as informações quantitativas mencionadas no documento"""
    
    print("\n" + "="*80)
    print("🔍 AUDITORIA DE DADOS - VERIFICAÇÃO QUANTITATIVA")
    print("="*80)
    
    verificacoes = []
    
    # 1. VERIFICAR TOTAL DE ARTIGOS
    total_artigos_real = len(df)
    total_artigos_documento = 41
    
    verificacoes.append({
        "item": "Total de artigos analisados",
        "documento": total_artigos_documento,
        "planilha": total_artigos_real,
        "status": "✅ CORRETO" if total_artigos_real == total_artigos_documento else "❌ DIVERGÊNCIA",
        "categoria": "Metadados Gerais"
    })
    
    print(f"\n1. TOTAL DE ARTIGOS:")
    print(f"   📄 Documento afirma: {total_artigos_documento} artigos")
    print(f"   📊 Planilha contém: {total_artigos_real} registros")
    print(f"   {'✅ CORRETO' if total_artigos_real == total_artigos_documento else '❌ DIVERGÊNCIA'}")
    
    # 2. VERIFICAR ODS MENCIONADOS
    print(f"\n2. VERIFICAÇÃO DOS ODS:")
    
    # Buscar colunas relacionadas aos ODS
    colunas_ods = [col for col in df.columns if 'ODS' in col.upper()]
    print(f"   📋 Colunas ODS encontradas: {colunas_ods}")
    
    if 'ODS Mencionados pelos Autores' in df.columns:
        coluna_ods = 'ODS Mencionados pelos Autores'
        
        # Contar referências gerais (17 trechos segundo documento)
        referencias_gerais = df[coluna_ods].fillna('').astype(str)
        count_geral = sum(1 for valor in referencias_gerais if 
                         'geral' in valor.lower() or 
                         'agenda 2030' in valor.lower() or
                         (not any(f'ods {i}' in valor.lower() for i in range(1, 18)) and 
                          valor.strip() and valor.lower() != 'nan'))
        
        verificacoes.append({
            "item": "Referências gerais aos ODS",
            "documento": 17,
            "planilha": count_geral,
            "status": "✅ CORRETO" if count_geral == 17 else "❌ DIVERGÊNCIA",
            "categoria": "ODS - Frequência"
        })
        
        print(f"   📊 Referências gerais (documento: 17, planilha: {count_geral})")
        
        # Verificar ODS específicos mencionados no documento
        ods_documento = {
            11: {"mencoes": 20, "percentual": 48.78},
            7: {"mencoes": 9, "percentual": 21.95},
            9: {"mencoes": 8, "percentual": 19.51},
            13: {"mencoes": 8, "percentual": 19.51},
            1: {"mencoes": 1, "percentual": 2.44},
            5: {"mencoes": 1, "percentual": 2.44},
            14: {"mencoes": 1, "percentual": 2.44}
        }
        
        for ods_num, dados_doc in ods_documento.items():
            # Contar menções específicas deste ODS com mais precisão
            # Usar regex para evitar confusão entre ODS 1 e ODS 11, ODS 10, etc.
            pattern = rf'\bods\s+{ods_num}\b'
            count_ods = sum(1 for valor in referencias_gerais if re.search(pattern, valor.lower()))
            percentual_real = round((count_ods / total_artigos_real) * 100, 2) if total_artigos_real > 0 else 0
            
            verificacoes.append({
                "item": f"ODS {ods_num} - Menções",
                "documento": dados_doc["mencoes"],
                "planilha": count_ods,
                "status": "✅ CORRETO" if count_ods == dados_doc["mencoes"] else "❌ DIVERGÊNCIA",
                "categoria": "ODS - Específicos"
            })
            
            verificacoes.append({
                "item": f"ODS {ods_num} - Percentual",
                "documento": dados_doc["percentual"],
                "planilha": percentual_real,
                "status": "✅ CORRETO" if abs(percentual_real - dados_doc["percentual"]) < 0.1 else "❌ DIVERGÊNCIA",
                "categoria": "ODS - Percentuais"
            })
            
            print(f"   📈 ODS {ods_num}: Doc({dados_doc['mencoes']}, {dados_doc['percentual']}%) vs Planilha({count_ods}, {percentual_real}%)")
    
    # 3. VERIFICAR TECNOLOGIAS EMERGENTES
    print(f"\n3. VERIFICAÇÃO DAS TECNOLOGIAS:")
    
    # Buscar colunas que podem conter informações sobre tecnologias
    colunas_tecnologia = [col for col in df.columns if any(palavra in col.lower() for palavra in 
                         ['palavra', 'chave', 'tecnologia', 'aspecto', 'categoria'])]
    print(f"   📋 Colunas de tecnologia encontradas: {colunas_tecnologia}")
    
    tecnologias_documento = {
        "IoT": {"estudos": 22, "percentual": 53.7},
        "IA": {"estudos": 19, "percentual": 46.3},
        "Big Data": {"estudos": 15, "percentual": 36.6},
        "Gêmeos Digitais": {"estudos": 8, "percentual": 19.5},
        "Metaverso": {"estudos": 5, "percentual": 12.2},
        "Impressão 3D": {"estudos": 3, "percentual": 7.3}
    }
    
    # Verificar se temos colunas de palavras-chave para análise
    if 'Palavras Chave' in df.columns or 'Palavras chave normalizadas e Traduzidas' in df.columns:
        coluna_palavras = 'Palavras chave normalizadas e Traduzidas' if 'Palavras chave normalizadas e Traduzidas' in df.columns else 'Palavras Chave'
        
        palavras_chave = df[coluna_palavras].fillna('').astype(str)
        texto_completo = ' '.join(palavras_chave).lower()
        
        for tech, dados_doc in tecnologias_documento.items():
            # Buscar variações da tecnologia
            termos_busca = []
            if tech == "IoT":
                termos_busca = ["iot", "internet of things", "internet das coisas"]
            elif tech == "IA":
                termos_busca = ["inteligência artificial", "artificial intelligence", "machine learning", "ai"]
            elif tech == "Big Data":
                termos_busca = ["big data", "dados massivos"]
            elif tech == "Gêmeos Digitais":
                termos_busca = ["digital twin", "gêmeo digital", "digital twins"]
            elif tech == "Metaverso":
                termos_busca = ["metaverse", "metaverso"]
            elif tech == "Impressão 3D":
                termos_busca = ["3d printing", "impressão 3d", "fabricação digital"]
            
            count_tech = 0
            for registro in palavras_chave:
                if any(termo in registro.lower() for termo in termos_busca):
                    count_tech += 1
            
            percentual_real = round((count_tech / total_artigos_real) * 100, 1) if total_artigos_real > 0 else 0
            
            verificacoes.append({
                "item": f"Tecnologia {tech} - Estudos",
                "documento": dados_doc["estudos"],
                "planilha": count_tech,
                "status": "✅ CORRETO" if count_tech == dados_doc["estudos"] else "❌ DIVERGÊNCIA",
                "categoria": "Tecnologias"
            })
            
            print(f"   🔬 {tech}: Doc({dados_doc['estudos']}, {dados_doc['percentual']}%) vs Planilha({count_tech}, {percentual_real}%)")
    
    # 4. VERIFICAR INFORMAÇÕES DE GOVERNANÇA
    print(f"\n4. VERIFICAÇÃO DE GOVERNANÇA E PARTICIPAÇÃO:")
    
    governanca_documento = {
        "Participação digital": {"estudos": 18, "percentual": 43.9},
        "Transparência": {"estudos": 15, "percentual": 36.6},
        "Colaboração intersetorial": {"estudos": 14, "percentual": 34.1},
        "Abordagens bottom-up": {"estudos": 12, "percentual": 29.3},
        "Inclusão digital": {"estudos": 10, "percentual": 24.4}
    }
    
    for tema, dados_doc in governanca_documento.items():
        # Esta verificação seria mais complexa, requer análise de conteúdo
        print(f"   🏛️ {tema}: Doc({dados_doc['estudos']}, {dados_doc['percentual']}%) - Requer análise de conteúdo")
    
    # 5. VERIFICAR PERSPECTIVA SOCIOTÉCNICA
    perspectiva_sociotecnica = round(73 * total_artigos_real / 100)
    verificacoes.append({
        "item": "Estudos com perspectiva sociotécnica",
        "documento": f"73% ({perspectiva_sociotecnica} estudos)",
        "planilha": "Requer análise de conteúdo",
        "status": "⚠️ VERIFICAÇÃO MANUAL NECESSÁRIA",
        "categoria": "Análise Qualitativa"
    })
    
    print(f"\n5. PERSPECTIVA SOCIOTÉCNICA:")
    print(f"   📊 Documento afirma: 73% dos estudos ({perspectiva_sociotecnica} estudos)")
    print(f"   ⚠️ Requer análise manual do conteúdo")
    
    return verificacoes

def verificar_pilares_csc(df):
    """Verifica informações sobre pilares do CSC com normalização de termos abreviados"""
    
    print(f"\n6. VERIFICAÇÃO DOS PILARES CSC:")
    
    # Buscar colunas relacionadas aos pilares CSC
    colunas_csc = [col for col in df.columns if 'csc' in col.lower() or 'pilar' in col.lower()]
    print(f"   📋 Colunas CSC encontradas: {colunas_csc}")
    
    # PRIMEIRO: Vamos ver exatamente o que temos na planilha
    if 'Pilar CSC' in df.columns:
        pilares_reais = df['Pilar CSC'].fillna('').astype(str)
        print(f"\n   🔍 ANÁLISE EXPLORATÓRIA - Primeiros 20 registros:")
        
        # Mostrar os primeiros registros para entender o padrão
        valores_unicos = set()
        for idx, registro in enumerate(pilares_reais[:20]):
            if registro and registro.lower() != 'nan' and registro.strip():
                print(f"      Registro {idx+1}: '{registro}'")
                # Coletar valores únicos para análise
                if ',' in registro:
                    for parte in registro.split(','):
                        valores_unicos.add(parte.strip().upper())
                else:
                    valores_unicos.add(registro.strip().upper())
        
        print(f"\n   📊 Valores únicos encontrados nos primeiros registros: {sorted(valores_unicos)}")
        
        # Fazer uma análise completa de todos os valores únicos
        todos_valores = set()
        for registro in pilares_reais:
            if registro and registro.lower() != 'nan' and registro.strip():
                if ',' in registro:
                    for parte in registro.split(','):
                        if parte.strip():
                            todos_valores.add(parte.strip().upper())
                else:
                    todos_valores.add(registro.strip().upper())
        
        print(f"\n   📋 TODOS os valores únicos na coluna Pilar CSC: {sorted(todos_valores)}")
        
        # Agora criar mapeamento baseado no que realmente existe
        mapeamento_pilares = {
            # Baseado no que encontramos, vamos mapear
        }
        
        # Detectar padrões automaticamente
        for valor in sorted(todos_valores):
            if not valor:
                continue
                
            # Tentar identificar o pilar baseado em palavras-chave
            if any(termo in valor for termo in ['TIC', 'TECNOL', 'INOV', 'TECH']):
                mapeamento_pilares[valor] = "Tecnologia e Inovação"
            elif any(termo in valor for termo in ['GOV', 'GOVERN']):
                mapeamento_pilares[valor] = "Governança"
            elif any(termo in valor for termo in ['MAM', 'AMB', 'MEIO']):
                mapeamento_pilares[valor] = "Meio Ambiente"
            elif any(termo in valor for termo in ['ENE', 'ENERG']):
                mapeamento_pilares[valor] = "Energia"
            elif any(termo in valor for termo in ['URB', 'URBAN']):
                mapeamento_pilares[valor] = "Urbanismo"
            elif any(termo in valor for termo in ['MOB', 'MOBIL']):
                mapeamento_pilares[valor] = "Mobilidade"
            elif any(termo in valor for termo in ['ECO', 'ECON']):
                mapeamento_pilares[valor] = "Economia"
            elif any(termo in valor for termo in ['EDU', 'EDUC']):
                mapeamento_pilares[valor] = "Educação"
            elif any(termo in valor for termo in ['SAU', 'SAUDE', 'HEALTH']):
                mapeamento_pilares[valor] = "Saúde"
            elif any(termo in valor for termo in ['SEG', 'SECUR']):
                mapeamento_pilares[valor] = "Segurança"
            elif any(termo in valor for termo in ['EMP', 'EMPR']):
                mapeamento_pilares[valor] = "Empreendedorismo"
            else:
                # Se não conseguiu identificar, manter o valor original
                mapeamento_pilares[valor] = valor.title()
        
        print(f"\n   🗺️ Mapeamento automático criado:")
        for original, mapeado in mapeamento_pilares.items():
            print(f"      '{original}' → '{mapeado}'")        
        # Agora processar todos os registros com o mapeamento correto
        contador_pilares = Counter()
        registros_processados = 0
        
        print(f"\n   � Processando todos os {len(pilares_reais)} registros...")
        
        for idx, registro in enumerate(pilares_reais):
            if registro and registro.lower() != 'nan' and registro.strip():
                registros_processados += 1
                
                # Separar múltiplos pilares se houver
                if ',' in registro:
                    pilares = [p.strip() for p in registro.split(',')]
                elif ';' in registro:
                    pilares = [p.strip() for p in registro.split(';')]
                elif '|' in registro:
                    pilares = [p.strip() for p in registro.split('|')]
                else:
                    pilares = [registro.strip()]
                
                pilares_normalizados = []
                
                for pilar in pilares:
                    if pilar:
                        pilar_upper = pilar.upper().strip()
                        pilar_normalizado = mapeamento_pilares.get(pilar_upper, pilar_upper)
                        
                        if pilar_normalizado not in pilares_normalizados:  # Evitar duplicatas
                            pilares_normalizados.append(pilar_normalizado)
                            contador_pilares[pilar_normalizado] += 1
                
                if idx < 10:  # Mostrar primeiros 10 processados
                    print(f"      Registro {idx+1}: '{registro}' → {pilares_normalizados}")
        
        print(f"\n   ✅ Processados {registros_processados} registros válidos de {len(pilares_reais)} total")
        
        print(f"\n   📊 Pilares consolidados na planilha (ordenados por frequência):")
        for pilar, count in contador_pilares.most_common():
            percentual_real = round((count / len(df)) * 100, 1)
            print(f"      {pilar}: {count} menções ({percentual_real}%)")
        
        # Dados do documento para comparação
        pilares_documento = {
            "Tecnologia e Inovação": {"mencoes": 32, "percentual": 85},
            "Governança": {"mencoes": 30, "percentual": 73},
            "Meio Ambiente": {"mencoes": 27, "percentual": 63},
            "Energia": {"mencoes": 23, "percentual": 59},
            "Urbanismo": {"mencoes": 19, "percentual": 46},
            "Mobilidade": {"mencoes": 18, "percentual": 44}
        }
        
        print(f"\n   📈 COMPARAÇÃO DETALHADA COM DOCUMENTO:")
        verificacoes_csc = []
        
        for pilar, dados_doc in pilares_documento.items():
            # Buscar correspondência exata ou aproximada
            count_real = contador_pilares.get(pilar, 0)
            
            # Se não encontrou correspondência exata, tentar buscar por palavras-chave
            if count_real == 0:
                for pilar_planilha, count_planilha in contador_pilares.items():
                    if pilar.upper() in pilar_planilha.upper() or pilar_planilha.upper() in pilar.upper():
                        count_real += count_planilha
                        print(f"         💡 Correspondência encontrada: '{pilar}' ≈ '{pilar_planilha}'")
            
            percentual_real = round((count_real / len(df)) * 100, 1)
            
            status_mencoes = "✅" if abs(count_real - dados_doc["mencoes"]) <= 2 else "❌"  # Tolerância de 2
            status_percentual = "✅" if abs(percentual_real - dados_doc["percentual"]) < 10 else "❌"  # Tolerância de 10%
            
            print(f"      🏗️ {pilar}:")
            print(f"         Menções - Doc: {dados_doc['mencoes']} | Planilha: {count_real} {status_mencoes}")
            print(f"         Percentual - Doc: {dados_doc['percentual']}% | Planilha: {percentual_real}% {status_percentual}")
            
            if count_real == 0:
                print(f"         ⚠️ ATENÇÃO: Pilar não encontrado ou com nome diferente na planilha")
            
            verificacoes_csc.append({
                "pilar": pilar,
                "documento_mencoes": dados_doc["mencoes"],
                "planilha_mencoes": count_real,
                "documento_percentual": dados_doc["percentual"],
                "planilha_percentual": percentual_real,
                "status_mencoes": status_mencoes,
                "status_percentual": status_percentual
            })
        
        return verificacoes_csc
    
    else:
        print("   ❌ Coluna 'Pilar CSC' não encontrada na planilha")
        return []

def verificar_indicadores_csc(df):
    """Verifica informações sobre indicadores específicos do CSC"""
    
    print(f"\n7. VERIFICAÇÃO DOS INDICADORES CSC:")
    
    if 'Indicadores CSC' not in df.columns:
        print("   ❌ Coluna 'Indicadores CSC' não encontrada na planilha")
        return []
    
    indicadores_csc = df['Indicadores CSC'].fillna('').astype(str)
    contador_indicadores = Counter()
    
    # Mapeamento de indicadores comuns do CSC (pode ser expandido)
    categorias_indicadores = {
        "SMART GRID": "Energia",
        "ENERGIA RENOVÁVEL": "Energia", 
        "EFICIÊNCIA ENERGÉTICA": "Energia",
        "GOVERNO ELETRÔNICO": "Governança",
        "DADOS ABERTOS": "Governança",
        "PARTICIPAÇÃO CIDADÃ": "Governança",
        "QUALIDADE DO AR": "Meio Ambiente",
        "GESTÃO DE RESÍDUOS": "Meio Ambiente",
        "MONITORAMENTO AMBIENTAL": "Meio Ambiente",
        "TRANSPORTE PÚBLICO": "Mobilidade",
        "MOBILIDADE SUSTENTÁVEL": "Mobilidade",
        "TRÂNSITO INTELIGENTE": "Mobilidade",
        "IOT": "Tecnologia e Inovação",
        "SENSORES": "Tecnologia e Inovação",
        "BIG DATA": "Tecnologia e Inovação",
        "INTELIGÊNCIA ARTIFICIAL": "Tecnologia e Inovação"
    }
    
    print(f"\n   🔍 Analisando {len([i for i in indicadores_csc if i.strip() and i.lower() != 'nan'])} registros de indicadores:")
    
    for idx, registro in enumerate(indicadores_csc):
        if registro and registro.lower() != 'nan' and registro.strip():
            print(f"      Registro {idx+1}: '{registro[:100]}...' " if len(registro) > 100 else f"      Registro {idx+1}: '{registro}'")
            
            # Separar múltiplos indicadores se houver
            indicadores = [i.strip() for i in registro.split(',')]
            
            for indicador in indicadores:
                if indicador:
                    indicador_upper = indicador.upper().strip()
                    contador_indicadores[indicador_upper] += 1
                    
                    # Verificar categoria do indicador
                    categoria_encontrada = None
                    for termo, categoria in categorias_indicadores.items():
                        if termo in indicador_upper:
                            categoria_encontrada = categoria
                            break
                    
                    if categoria_encontrada:
                        print(f"         → '{indicador}' → Categoria: {categoria_encontrada}")
    
    print(f"\n   📊 Top 10 indicadores mais mencionados:")
    for indicador, count in contador_indicadores.most_common(10):
        percentual = round((count / len(df)) * 100, 1)
        print(f"      {indicador}: {count} menções ({percentual}%)")
    
    return dict(contador_indicadores)

def gerar_relatorio_auditoria(verificacoes):
    """Gera relatório final da auditoria"""
    
    print("\n" + "="*80)
    print("📋 RELATÓRIO DE AUDITORIA - RESUMO EXECUTIVO")
    print("="*80)
    
    total_verificacoes = len(verificacoes)
    corretas = sum(1 for v in verificacoes if "✅ CORRETO" in v["status"])
    divergencias = sum(1 for v in verificacoes if "❌ DIVERGÊNCIA" in v["status"])
    manuais = sum(1 for v in verificacoes if "⚠️" in v["status"])
    
    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"   • Total de verificações: {total_verificacoes}")
    print(f"   • ✅ Corretas: {corretas}")
    print(f"   • ❌ Divergências: {divergencias}")
    print(f"   • ⚠️ Verificação manual necessária: {manuais}")
    print(f"   • 📈 Taxa de precisão: {round((corretas/total_verificacoes)*100, 1)}%")
    
    # Agrupar por categoria
    categorias = {}
    for v in verificacoes:
        cat = v["categoria"]
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(v)
    
    print(f"\n📂 ANÁLISE POR CATEGORIA:")
    for categoria, items in categorias.items():
        corretas_cat = sum(1 for i in items if "✅ CORRETO" in i["status"])
        total_cat = len(items)
        print(f"   🏷️ {categoria}: {corretas_cat}/{total_cat} corretas")
    
    # Listar divergências principais
    if divergencias > 0:
        print(f"\n⚠️ PRINCIPAIS DIVERGÊNCIAS ENCONTRADAS:")
        for v in verificacoes:
            if "❌ DIVERGÊNCIA" in v["status"]:
                print(f"   • {v['item']}: Doc({v['documento']}) vs Planilha({v['planilha']})")
    
    # Salvar relatório detalhado
    relatorio = {
        "data_auditoria": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resumo": {
            "total_verificacoes": total_verificacoes,
            "corretas": corretas,
            "divergencias": divergencias,
            "verificacao_manual": manuais,
            "taxa_precisao": round((corretas/total_verificacoes)*100, 1)
        },
        "verificacoes_detalhadas": verificacoes,
        "recomendacoes": [
            "Revisar divergências encontradas na comparação quantitativa",
            "Realizar análise manual das informações qualitativas",
            "Verificar consistência entre fonte de dados e documento",
            "Atualizar documento com dados corretos da planilha"
        ]
    }
    
    with open("relatorio_auditoria_dissertacao.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Relatório detalhado salvo em: relatorio_auditoria_dissertacao.json")
    
    return relatorio

def analisar_ods_detalhado(df):
    """Análise detalhada e precisa dos ODS para evitar confusões entre números"""
    
    print(f"\n🔍 ANÁLISE DETALHADA DOS ODS (evitando confusão entre números)")
    
    if 'ODS Mencionados pelos Autores' not in df.columns:
        print("❌ Coluna 'ODS Mencionados pelos Autores' não encontrada")
        return {}
    
    coluna_ods = 'ODS Mencionados pelos Autores'
    referencias_ods = df[coluna_ods].fillna('').astype(str)
    
    # Contadores específicos para cada ODS
    contadores_ods = {}
    
    # Lista todos os ODS de 1 a 17
    for i in range(1, 18):
        contadores_ods[i] = 0
    
    # Contador para referências gerais
    count_geral = 0
    
    print(f"\n📊 Analisando {len(referencias_ods)} registros...")
    
    for idx, valor in enumerate(referencias_ods):
        valor_clean = valor.strip().lower()
        
        if not valor_clean or valor_clean == 'nan':
            continue
            
        print(f"   Registro {idx+1}: '{valor[:100]}...' " if len(valor) > 100 else f"   Registro {idx+1}: '{valor}'")
        
        # Verificar se é referência geral
        termos_gerais = ['geral', 'agenda 2030', 'todos os ods', 'objetivos de desenvolvimento sustentável']
        if any(termo in valor_clean for termo in termos_gerais):
            count_geral += 1
            print(f"      → Classificado como: REFERÊNCIA GERAL")
            continue
        
        # Verificar ODS específicos usando regex mais preciso
        ods_encontrados = []
        
        # Padrões para detectar ODS específicos
        padroes = [
            r'\bods\s+(\d{1,2})\b',           # "ODS 11", "ODS 1", etc.
            r'\bsdg\s+(\d{1,2})\b',           # "SDG 11", "SDG 1", etc.
            r'\bobjetivo\s+(\d{1,2})\b',      # "Objetivo 11", etc.
            r'\bgoal\s+(\d{1,2})\b'           # "Goal 11", etc.
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, valor_clean)
            for match in matches:
                ods_num = int(match)
                if 1 <= ods_num <= 17:
                    ods_encontrados.append(ods_num)
        
        # Remover duplicatas mantendo ordem
        ods_encontrados = list(dict.fromkeys(ods_encontrados))
        
        if ods_encontrados:
            print(f"      → ODS específicos encontrados: {ods_encontrados}")
            for ods_num in ods_encontrados:
                contadores_ods[ods_num] += 1
        else:
            # Se não encontrou padrão específico, mas não é geral, verificar manualmente
            if valor_clean and not any(char.isdigit() for char in valor_clean):
                count_geral += 1
                print(f"      → Sem número específico, classificado como: REFERÊNCIA GERAL")
            else:
                print(f"      → ⚠️ Padrão não reconhecido, requer verificação manual")
    
    print(f"\n📈 RESULTADOS DA ANÁLISE:")
    print(f"   📊 Referências gerais: {count_geral}")
    
    for ods_num in range(1, 18):
        if contadores_ods[ods_num] > 0:
            percentual = round((contadores_ods[ods_num] / len(df)) * 100, 2)
            print(f"   📈 ODS {ods_num}: {contadores_ods[ods_num]} menções ({percentual}%)")
    
    return {
        'geral': count_geral,
        'especificos': contadores_ods,
        'total_registros': len(df)
    }

def main():
    """Função principal da auditoria"""
    
    print("🔍 INICIANDO AUDITORIA DE DADOS DA DISSERTAÇÃO")
    print("="*80)
    
    # Carregar dados
    df = extrair_dados_planilha()
    if df is None:
        return
    
    # Análise detalhada dos ODS primeiro
    print("\n" + "="*80)
    print("🎯 ANÁLISE DETALHADA DOS ODS (Evitando confusão entre números)")
    print("="*80)
    resultados_ods = analisar_ods_detalhado(df)
    
    # Realizar verificações quantitativas
    verificacoes = verificar_informacoes_quantitativas(df)
      # Verificar pilares CSC
    verificacoes_csc = verificar_pilares_csc(df)
    
    # Verificar indicadores CSC
    indicadores_csc = verificar_indicadores_csc(df)
    
    # Comparar resultados da análise detalhada com o documento
    if resultados_ods:
        print("\n" + "="*80)
        print("📊 COMPARAÇÃO DETALHADA: DOCUMENTO vs PLANILHA")
        print("="*80)
        
        # Dados do documento
        ods_documento = {
            11: {"mencoes": 20, "percentual": 48.78},
            7: {"mencoes": 9, "percentual": 21.95},
            9: {"mencoes": 8, "percentual": 19.51},
            13: {"mencoes": 8, "percentual": 19.51},
            1: {"mencoes": 1, "percentual": 2.44},
            5: {"mencoes": 1, "percentual": 2.44},
            14: {"mencoes": 1, "percentual": 2.44}
        }
        
        print(f"\n📋 REFERÊNCIAS GERAIS:")
        print(f"   Documento: 17 trechos")
        print(f"   Planilha: {resultados_ods['geral']} trechos")
        print(f"   Status: {'✅ CORRETO' if resultados_ods['geral'] == 17 else '❌ DIVERGÊNCIA'}")
        
        print(f"\n📈 ODS ESPECÍFICOS:")
        for ods_num, dados_doc in ods_documento.items():
            count_planilha = resultados_ods['especificos'][ods_num]
            percentual_planilha = round((count_planilha / resultados_ods['total_registros']) * 100, 2)
            
            status_mencoes = "✅" if count_planilha == dados_doc["mencoes"] else "❌"
            status_percentual = "✅" if abs(percentual_planilha - dados_doc["percentual"]) < 0.1 else "❌"
            
            print(f"   ODS {ods_num}:")
            print(f"      Menções - Doc: {dados_doc['mencoes']} | Planilha: {count_planilha} {status_mencoes}")
            print(f"      Percentual - Doc: {dados_doc['percentual']}% | Planilha: {percentual_planilha}% {status_percentual}")
    
    # Gerar relatório final
    relatorio = gerar_relatorio_auditoria(verificacoes)
    
    print(f"\n✅ AUDITORIA CONCLUÍDA")
    print(f"📋 Consulte o arquivo 'relatorio_auditoria_dissertacao.json' para detalhes completos")

if __name__ == "__main__":
    main()
