#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar a visualização corrigida usando o logo circular dos ODS
"""

import re

def atualizar_visualizacao_corrigida():
    """Atualiza a visualização corrigida para usar o logo circular"""
    
    file_path = 'visualizacao_icones_ods_corrigida.html'
    
    try:
        # Ler o arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ Arquivo lido: {len(content)} caracteres")
        
        # Padrão para encontrar os containers ODS Geral
        pattern = r'<div class="ods-geral-container"[^>]*>.*?</div>'
        
        # Novo conteúdo para substituir
        replacement = '''<div class="ods-geral-container" title="ODS Geral - Múltiplos Objetivos">
    <img src="logo-sepado.png" alt="ODS Geral" title="Objetivos de Desenvolvimento Sustentável" 
         style="width: 50px; height: 50px; border-radius: 50%; border: 2px solid #FFD700;">
    <span class="ods-geral-label" style="margin-left: 5px; font-size: 11px; font-weight: bold;">GERAL</span>
</div>'''
        
        # Fazer a substituição
        content_updated = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Contar substituições
        matches_found = len(re.findall(pattern, content, flags=re.DOTALL))
        
        print(f"🔄 Encontradas {matches_found} ocorrências de ODS Geral")
        
        # Salvar arquivo atualizado
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_updated)
        
        print(f"✅ Arquivo atualizado: {file_path}")
        print(f"🎯 Logo circular aplicado em {matches_found} locais")
        
        # Criar versão backup da original
        backup_path = 'visualizacao_icones_ods_corrigida_BACKUP.html'
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)  # Salva versão original
            print(f"💾 Backup salvo: {backup_path}")
        except Exception as e:
            print(f"⚠️ Não foi possível criar backup: {e}")
            
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")

def verificar_resultado():
    """Verifica se a atualização foi bem-sucedida"""
    
    file_path = 'visualizacao_icones_ods_corrigida.html'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se o logo está presente
        logo_count = content.count('logo-sepado.png')
        geral_count = content.count('ods-geral-container')
        
        print(f"\n🔍 VERIFICAÇÃO:")
        print(f"   Logo circular encontrado: {logo_count} vezes")
        print(f"   Containers ODS Geral: {geral_count}")
        
        if logo_count > 0:
            print("✅ Atualização bem-sucedida!")
        else:
            print("❌ Logo não encontrado - pode haver problema")
            
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")

if __name__ == "__main__":
    print("🚀 Atualizando visualização para usar logo circular dos ODS...")
    atualizar_visualizacao_corrigida()
    verificar_resultado()
    print("✅ Processo concluído!")
