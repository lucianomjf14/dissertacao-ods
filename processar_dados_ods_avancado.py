#!/usr/bin/env python3
"""
Script avançado para limpeza e organização do projeto
Remove arquivos desnecessários e mantém apenas os essenciais
"""

import os
import shutil
import json
from datetime import datetime

def criar_backup():
    """Criar backup dos arquivos importantes antes da limpeza"""
    print("🔄 Criando backup dos arquivos importantes...")
    
    backup_dir = "backup_antes_limpeza"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    arquivos_importantes = [
        "visualizacao_FINAL_FUNCIONAL.html",
        "dados_javascript.js", 
        "Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx",
        "processar_dados_ods.py"
    ]
    
    for arquivo in arquivos_importantes:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, backup_dir)
            print(f"  ✅ Backup criado: {arquivo}")
    
    print(f"📁 Backup salvo em: {backup_dir}/")
    return backup_dir

def listar_arquivos_desnecessarios():
    """Identificar arquivos que podem ser removidos"""
    
    # Arquivos HTML antigos/duplicados (manter apenas o FINAL_FUNCIONAL)
    htmls_desnecessarios = [
        "visualizacao_MELHORADA_FINAL.html",
        "visualizacao_interativa_melhorada.html", 
        "visualizacao_interativa.html",
        "visualizacao_icones_ods_corrigida_BACKUP.html",
        "visualizacao_icones_ods_corrigida.html",
        "visualizacao_correspondencia_corrigida.html",
        "visualizacao_corpus.html",
        "visualizacao_COM_METRICAS_ODS_novo.html",
        "visualizacao_COM_METRICAS_ODS_CORRETO.html", 
        "visualizacao_COM_METRICAS_ODS.html",
        "visualizacao_com_icones_ods.html",
        "teste_dados.html",
        "relatorio_verificacao.html"
    ]
    
    # Scripts Python antigos/duplicados
    scripts_desnecessarios = [
        "analisar_ods.py",
        "atualizar_logo_circular.py",
        "corrigir_correspondencia_colunas.py", 
        "corrigir_funcionalidades_selecao.py",
        "criar_versao_final_funcional.py",
        "criar_versao_funcional.py",
        "criar_visualizacao_melhorada.py",
        "demo_sincronizador.py",
        "diagnosticar_colunas.py",
        "documentar_colapsavel.py",
        "documentar_tipos_visualizacao.py",
        "limpar_debug.py",
        "servidor_atualizacao.py",
        "servidor_atualizacao_corrigido.py", 
        "sincronizar_excel_html.py",
        "sincronizar_excel_html_v2.py",
        "validar_funcionalidade.py",
        "verificar_correspondencia.py",
        "verificar_info_academica.py",
        "verificar_logo_circular.py",
        "verificar_melhorias_finais.py",
        "verificar_tipos_visualizacao.py",
        "visualizador_interativo.py",
        "visualizador_melhorado.py",
        "visualizador_web.py"
    ]
    
    # Arquivos de documentação antigas
    docs_desnecessarios = [
        "FUNCIONALIDADE_RESOLVIDA.md",
        "INSTRUCOES_TABELA_ABNT.md",
        "INSTRUÇÕES_ATUALIZAÇÃO_AUTOMÁTICA.md", 
        "MELHORIAS_IMPLEMENTADAS.md",
        "RESUMO_IMPLEMENTAÇÃO_COMPLETA.md",
        "SECAO_COLAPSAVEL_IMPLEMENTADA.md",
        "SISTEMA_DETECCAO_MUDANCAS_IMPLEMENTADO.md",
        "TESTE_RESUMO.md",
        "TIPOS_VISUALIZACAO_IMPLEMENTADOS.md"
    ]
    
    # Arquivos temporários e de dados duplicados
    temp_desnecessarios = [
        "dados_completos_ods.json",  # duplicação do dados_javascript.js
        "metadata_estrutural.json",
        "logo_ods_circular.svg",
        "ods_logo_circular.svg",  # manter apenas logo-sepado.png
        "iniciar_servidor.bat"
    ]
    
    # Arquivos LaTeX (se não precisar mais)
    latex_desnecessarios = [
        "tabela_abnt.tex",
        "tabela_abnt_final.tex", 
        "tabela_apendice_compacta.tex",
        "tabela_apendice_longitudinal.tex"
    ]
    
    return {
        "HTMLs antigos": htmls_desnecessarios,
        "Scripts Python antigos": scripts_desnecessarios, 
        "Documentação antiga": docs_desnecessarios,
        "Arquivos temporários": temp_desnecessarios,
        "Arquivos LaTeX": latex_desnecessarios
    }

def arquivos_essenciais():
    """Lista dos arquivos que DEVEM ser mantidos"""
    return [
        # Arquivo principal
        "visualizacao_FINAL_FUNCIONAL.html",
        
        # Dados essenciais
        "dados_javascript.js",
        "Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx",
        
        # Scripts essenciais
        "processar_dados_ods.py",
        "gerar_tabela_abnt.py",
        "gerar_tabela_apendice_abnt.py", 
        "gerar_visualizacao_icones_ods.py",
        
        # Imagens essenciais
        "logo-sepado.png",
        
        # Pastas essenciais
        "ícones oficiais - CSC/",
        "Ícones oficiais - ODS/",
        
        # Ambiente virtual
        ".venv/",
        "__pycache__/"
    ]

def executar_limpeza(modo_dry_run=True):
    """Executar a limpeza dos arquivos"""
    
    print("🧹 INICIANDO LIMPEZA DO PROJETO")
    print("=" * 50)
    
    if modo_dry_run:
        print("⚠️  MODO DRY RUN - Nenhum arquivo será removido")
        print("   Para executar a limpeza real, execute: python processar_dados_ods_avancado.py --execute")
    else:
        print("🚨 MODO EXECUÇÃO - Arquivos SERÃO removidos!")
        backup_dir = criar_backup()
    
    arquivos_para_remover = listar_arquivos_desnecessarios()
    essenciais = arquivos_essenciais()
    
    total_removidos = 0
    tamanho_liberado = 0
    
    print(f"\n📋 RELATÓRIO DE LIMPEZA:")
    print("-" * 30)
    
    for categoria, arquivos in arquivos_para_remover.items():
        print(f"\n📂 {categoria}:")
        categoria_removidos = 0
        
        for arquivo in arquivos:
            if os.path.exists(arquivo) and arquivo not in essenciais:
                tamanho = os.path.getsize(arquivo) if os.path.isfile(arquivo) else 0
                tamanho_liberado += tamanho
                
                if modo_dry_run:
                    print(f"  🗑️  {arquivo} ({tamanho/1024:.1f} KB)")
                else:
                    try:
                        if os.path.isfile(arquivo):
                            os.remove(arquivo)
                        elif os.path.isdir(arquivo):
                            shutil.rmtree(arquivo)
                        print(f"  ✅ Removido: {arquivo} ({tamanho/1024:.1f} KB)")
                    except Exception as e:
                        print(f"  ❌ Erro ao remover {arquivo}: {e}")
                
                categoria_removidos += 1
                total_removidos += 1
            elif arquivo in essenciais:
                print(f"  🔒 Protegido: {arquivo}")
            elif not os.path.exists(arquivo):
                print(f"  ❓ Não existe: {arquivo}")
        
        if categoria_removidos == 0:
            print(f"  ✨ Nenhum arquivo para remover nesta categoria")
    
    print(f"\n📊 RESUMO:")
    print(f"  Total de arquivos processados: {total_removidos}")
    print(f"  Espaço liberado: {tamanho_liberado/1024/1024:.1f} MB")
    
    if not modo_dry_run:
        # Criar relatório da limpeza
        relatorio = {
            "timestamp": datetime.now().isoformat(),
            "backup_dir": backup_dir if 'backup_dir' in locals() else None,
            "arquivos_removidos": total_removidos,
            "espaco_liberado_mb": round(tamanho_liberado/1024/1024, 2),
            "arquivos_mantidos": essenciais
        }
        
        with open("relatorio_limpeza.json", "w", encoding="utf-8") as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Relatório salvo em: relatorio_limpeza.json")
    
    print(f"\n✅ Limpeza {'simulada' if modo_dry_run else 'concluída'} com sucesso!")

def mostrar_estrutura_final():
    """Mostrar como ficará a estrutura final do projeto"""
    print("\n🏗️  ESTRUTURA FINAL DO PROJETO:")
    print("=" * 40)
    
    essenciais = arquivos_essenciais()
    
    for item in sorted(essenciais):
        if os.path.exists(item):
            if os.path.isdir(item):
                print(f"📁 {item}")
                # Mostrar alguns arquivos dentro das pastas importantes
                if item in ["ícones oficiais - CSC/", "Ícones oficiais - ODS/"]:
                    try:
                        arquivos = os.listdir(item)[:3]  # Mostrar apenas os primeiros 3
                        for arq in arquivos:
                            print(f"   🖼️  {arq}")
                        if len(os.listdir(item)) > 3:
                            print(f"   ... e mais {len(os.listdir(item)) - 3} arquivos")
                    except:
                        pass
            else:
                tamanho = os.path.getsize(item) / 1024 if os.path.isfile(item) else 0
                print(f"📄 {item} ({tamanho:.1f} KB)")
        else:
            print(f"❓ {item} (não encontrado)")

if __name__ == "__main__":
    import sys
    
    # Verificar argumentos da linha de comando
    if "--execute" in sys.argv:
        modo_dry_run = False
    else:
        modo_dry_run = True
    
    try:
        executar_limpeza(modo_dry_run)
        mostrar_estrutura_final()
        
        if modo_dry_run:
            print(f"\n💡 Para executar a limpeza real:")
            print(f"   python processar_dados_ods_avancado.py --execute")
            
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
        sys.exit(1)
