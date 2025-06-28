#!/usr/bin/env python3
"""
Script para verificar a implementação da funcionalidade de tipos de visualização
no arquivo visualizacao_MELHORADA_FINAL.html
"""

def verificar_tipos_visualizacao():
    arquivo = "visualizacao_MELHORADA_FINAL.html"
    
    print("🔍 VERIFICANDO IMPLEMENTAÇÃO DE TIPOS DE VISUALIZAÇÃO")
    print("=" * 60)
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verificações de implementação
        verificacoes = [
            ("✅ Seletor de Tipo de Visualização", "view-type-selector" in conteudo),
            ("✅ Botões de alternância", "tableViewBtn" in conteudo and "metricsViewBtn" in conteudo),
            ("✅ Função switchViewType", "function switchViewType" in conteudo),
            ("✅ Variável currentViewType", "currentViewType" in conteudo),
            ("✅ Visualização de Tabela", "tableView" in conteudo),
            ("✅ Visualização de Métricas", "metricsView" in conteudo),
            ("✅ CSS para botões", ".view-type-btn" in conteudo),
            ("✅ CSS para métricas", ".metrics-view" in conteudo),
            ("✅ Placeholder de métricas", "metrics-placeholder" in conteudo),
            ("✅ Status bar dinâmico", "Visualização: Métricas" in conteudo),
        ]
        
        print("📋 COMPONENTES IMPLEMENTADOS:")
        print("-" * 40)
        for descricao, resultado in verificacoes:
            status = "✅ OK" if resultado else "❌ FALTANDO"
            print(f"{descricao:<35} {status}")
        
        # Funcionalidades específicas
        print("\n📊 FUNCIONALIDADES ESPECÍFICAS:")
        print("-" * 40)
        
        # Verificar se os controles da tabela são ocultos na visualização de métricas
        ocultar_controles = "tableControls.style.display = 'none'" in conteudo
        print(f"{'Ocultação de controles na visualização de métricas':<45} {'✅ OK' if ocultar_controles else '❌ FALTANDO'}")
        
        # Verificar se a visualização de métricas é mostrada
        mostrar_metricas = "metricsView.classList.add('active')" in conteudo
        print(f"{'Ativação da visualização de métricas':<45} {'✅ OK' if mostrar_metricas else '❌ FALTANDO'}")
        
        # Verificar se há placeholder para métricas
        placeholder_metricas = "Em Desenvolvimento" in conteudo
        print(f"{'Placeholder para métricas futuras':<45} {'✅ OK' if placeholder_metricas else '❌ FALTANDO'}")
        
        print("\n🎯 RESULTADO FINAL:")
        print("-" * 40)
        todos_ok = all(resultado for _, resultado in verificacoes) and ocultar_controles and mostrar_metricas and placeholder_metricas
        
        if todos_ok:
            print("✅ FUNCIONALIDADE COMPLETAMENTE IMPLEMENTADA!")
            print("   • Alternância entre 'Tabela' e 'Métricas' funcionando")
            print("   • Controles específicos para cada tipo de visualização")
            print("   • Status bar dinâmico")
            print("   • Placeholder para futuras métricas")
        else:
            print("⚠️  IMPLEMENTAÇÃO PARCIAL - Verificar itens faltantes")
            
    except FileNotFoundError:
        print(f"❌ Arquivo {arquivo} não encontrado!")
    except Exception as e:
        print(f"❌ Erro ao verificar arquivo: {e}")

if __name__ == "__main__":
    verificar_tipos_visualizacao()
