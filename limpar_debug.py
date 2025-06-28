#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar debug da versão FINAL FUNCIONAL
"""

def limpar_debug_final_funcional():
    """Remove todos os logs de debug da versão final funcional"""
    
    file_path = 'visualizacao_FINAL_FUNCIONAL.html'
    
    try:
        # Ler arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ Arquivo lido: {len(content)} caracteres")
        
        # Remover todas as linhas com logDebug
        lines = content.split('\n')
        clean_lines = []
        
        for line in lines:
            # Pular linhas com debug
            if ('logDebug(' in line or 
                'console.log(' in line or
                'debugLog' in line or
                'debug-info' in line.lower()):
                continue
            clean_lines.append(line)
        
        # Remover função logDebug completa
        content_clean = '\n'.join(clean_lines)
        
        # Remover bloco da função logDebug
        import re
        content_clean = re.sub(
            r'function logDebug\(.*?\n\s*}', 
            '', 
            content_clean, 
            flags=re.DOTALL
        )
        
        # Remover div debug-info
        content_clean = re.sub(
            r'<div class="debug-info".*?</div>', 
            '', 
            content_clean, 
            flags=re.DOTALL
        )
        
        # Salvar versão limpa
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_clean)
        
        print(f"✅ Debug removido e arquivo atualizado")
        print(f"📝 Tamanho final: {len(content_clean)} caracteres")
        
        # Verificar se ainda tem debug
        if 'logDebug' in content_clean or 'console.log' in content_clean:
            print("⚠️ Ainda existem algumas referências de debug")
        else:
            print("✅ Todo debug removido com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🧹 Limpando debug da versão FINAL FUNCIONAL...")
    limpar_debug_final_funcional()
    print("✅ Limpeza concluída!")
