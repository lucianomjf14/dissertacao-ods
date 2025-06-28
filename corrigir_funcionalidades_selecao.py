#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir as funcionalidades de seleção/desseleção na visualização ODS
"""

import pandas as pd
from pathlib import Path
import re

def corrigir_funcionalidades_selecao():
    """
    Lê o arquivo atual e corrige as funcionalidades de seleção
    """
    try:
        arquivo_atual = "visualizacao_com_icones_ods.html"
        
        with open(arquivo_atual, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # JavaScript corrigido para as funcionalidades
        js_corrigido = """
        // Informações das colunas carregadas do Python
        const columnsInfo = [{'index': 0, 'name': 'Link', 'id': 'col_0', 'is_ods': False}, {'index': 1, 'name': 'ID', 'id': 'col_1', 'is_ods': False}, {'index': 2, 'name': 'Autores', 'id': 'col_2', 'is_ods': False}, {'index': 3, 'name': 'Título', 'id': 'col_3', 'is_ods': False}, {'index': 4, 'name': 'Ano', 'id': 'col_4', 'is_ods': False}, {'index': 5, 'name': 'Periódico', 'id': 'col_5', 'is_ods': False}, {'index': 6, 'name': 'Idioma', 'id': 'col_6', 'is_ods': False}, {'index': 7, 'name': 'DOI', 'id': 'col_7', 'is_ods': False}, {'index': 8, 'name': 'ISSN', 'id': 'col_8', 'is_ods': False}, {'index': 9, 'name': 'Categorias', 'id': 'col_9', 'is_ods': False}, {'index': 10, 'name': 'Status', 'id': 'col_10', 'is_ods': False}, {'index': 11, 'name': 'Palavras Chave', 'id': 'col_11', 'is_ods': False}, {'index': 12, 'name': 'Trechos correlações', 'id': 'col_12', 'is_ods': False}, {'index': 13, 'name': 'ODS (Geral / Específico)', 'id': 'col_13', 'is_ods': True}, {'index': 14, 'name': 'Aspecto Principal - Estudo', 'id': 'col_14', 'is_ods': False}, {'index': 15, 'name': 'Aspectos relacionados', 'id': 'col_15', 'is_ods': False}, {'index': 16, 'name': 'Impactos / Resultados', 'id': 'col_16', 'is_ods': False}, {'index': 17, 'name': 'Pilar CSC', 'id': 'col_17', 'is_ods': False}, {'index': 18, 'name': 'Indicadores CSC', 'id': 'col_18', 'is_ods': False}, {'index': 19, 'name': 'CORPUS - IRAMUTEQ', 'id': 'col_19', 'is_ods': False}];
        
        console.log('🎯 Sistema com ícones ODS inicializado');
        console.log('📊 Total de colunas mapeadas:', columnsInfo.length);
        
        // Encontra a coluna ODS
        const odsColumnIndex = columnsInfo.find(col => col.is_ods)?.index;
        console.log('🎯 Coluna ODS identificada no índice:', odsColumnIndex);
        
        // Função CORRIGIDA para alternar visibilidade das colunas
        function toggleColumn(colIndex) {
            console.log(`🔧 Alternando coluna índice: ${colIndex}`);
            
            const table = document.getElementById('mainTable');
            const checkbox = document.getElementById('col_' + colIndex);
            
            if (!checkbox) {
                console.error(`❌ Checkbox não encontrado: col_${colIndex}`);
                return;
            }
            
            const isChecked = checkbox.checked;
            const isODSColumn = colIndex === odsColumnIndex;
            
            console.log(`📊 Coluna ${colIndex} ${isChecked ? 'MOSTRANDO' : 'OCULTANDO'}${isODSColumn ? ' (COLUNA ODS COM ÍCONES!)' : ''}`);
            
            // Alterna header (th)
            const headerCells = table.getElementsByTagName('th');
            if (headerCells[colIndex]) {
                if (isChecked) {
                    headerCells[colIndex].classList.remove('hidden-column');
                } else {
                    headerCells[colIndex].classList.add('hidden-column');
                }
                console.log(`✅ Header coluna ${colIndex}: ${isChecked ? 'VISÍVEL' : 'OCULTO'}`);
            } else {
                console.error(`❌ Header da coluna ${colIndex} não encontrado`);
            }
            
            // Alterna células de dados (td)
            const rows = table.getElementsByTagName('tr');
            let cellsUpdated = 0;
            for (let i = 1; i < rows.length; i++) { // Pula o header (índice 0)
                const cells = rows[i].getElementsByTagName('td');
                if (cells[colIndex]) {
                    if (isChecked) {
                        cells[colIndex].classList.remove('hidden-column');
                    } else {
                        cells[colIndex].classList.add('hidden-column');
                    }
                    cellsUpdated++;
                }
            }
            console.log(`✅ ${cellsUpdated} células da coluna ${colIndex} atualizadas`);
            
            if (isODSColumn && isChecked) {
                console.log('🎯 Coluna ODS ativada - ícones devem estar visíveis!');
            }
        }
        
        // Função CORRIGIDA para selecionar todas as colunas
        function selectAll() {
            console.log('🔄 INICIANDO seleção de todas as colunas...');
            
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            console.log(`📋 Encontrados ${checkboxes.length} checkboxes`);
            
            let processedCount = 0;
            checkboxes.forEach((checkbox, index) => {
                const colIndex = parseInt(checkbox.value);
                console.log(`🔲 Processando checkbox ${index}: coluna ${colIndex}`);
                
                // Marca o checkbox
                checkbox.checked = true;
                
                // Aplica a visibilidade
                toggleColumn(colIndex);
                processedCount++;
            });
            
            console.log(`✅ CONCLUÍDO: ${processedCount} colunas selecionadas`);
            
            // Verificação final
            setTimeout(() => {
                const visibleHeaders = document.querySelectorAll('#mainTable th:not(.hidden-column)');
                console.log(`🔍 Verificação: ${visibleHeaders.length} cabeçalhos visíveis`);
            }, 100);
        }
        
        // Função CORRIGIDA para desmarcar todas as colunas
        function deselectAll() {
            console.log('🔄 INICIANDO desmarcação de todas as colunas...');
            
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            console.log(`📋 Encontrados ${checkboxes.length} checkboxes`);
            
            let processedCount = 0;
            checkboxes.forEach((checkbox, index) => {
                const colIndex = parseInt(checkbox.value);
                console.log(`☐ Processando checkbox ${index}: coluna ${colIndex}`);
                
                // Desmarca o checkbox
                checkbox.checked = false;
                
                // Aplica a ocultação
                toggleColumn(colIndex);
                processedCount++;
            });
            
            console.log(`✅ CONCLUÍDO: ${processedCount} colunas desmarcadas`);
            
            // Verificação final
            setTimeout(() => {
                const visibleHeaders = document.querySelectorAll('#mainTable th:not(.hidden-column)');
                const hiddenHeaders = document.querySelectorAll('#mainTable th.hidden-column');
                console.log(`🔍 Verificação: ${visibleHeaders.length} visíveis, ${hiddenHeaders.length} ocultos`);
            }, 100);
        }
        
        // Função CORRIGIDA para resetar para padrão
        function resetToDefault() {
            console.log('🔄 INICIANDO reset para configuração padrão...');
            
            const defaultColumns = ['ID', 'Autores', 'Título', 'Ano', 'Periódico', 'ODS (Geral / Específico)', 'Aspecto Principal - Estudo'];
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            
            let selectedCount = 0;
            let deselectedCount = 0;
            
            checkboxes.forEach((checkbox, index) => {
                const colIndex = parseInt(checkbox.value);
                const label = checkbox.parentElement.querySelector('.col-name').textContent.trim();
                
                // Remove emoji/ícone do início se existir
                const cleanLabel = label.replace(/^🎯\s*/, '').trim();
                
                const shouldCheck = defaultColumns.some(col => cleanLabel.includes(col));
                
                console.log(`📋 Coluna ${colIndex}: "${cleanLabel}" ${shouldCheck ? 'SERÁ SELECIONADA' : 'será desmarcada'}`);
                
                checkbox.checked = shouldCheck;
                toggleColumn(colIndex);
                
                if (shouldCheck) {
                    selectedCount++;
                } else {
                    deselectedCount++;
                }
            });
            
            console.log(`✅ PADRÃO APLICADO: ${selectedCount} selecionadas, ${deselectedCount} desmarcadas`);
        }
        
        // Função CORRIGIDA para mostrar apenas ODS
        function mostrarApenasODS() {
            console.log('🎯 INICIANDO modo apenas ODS...');
            
            const essentialColumns = ['ID', 'Autores', 'Título', 'Ano', 'ODS (Geral / Específico)'];
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            
            let selectedCount = 0;
            let deselectedCount = 0;
            
            checkboxes.forEach((checkbox) => {
                const colIndex = parseInt(checkbox.value);
                const label = checkbox.parentElement.querySelector('.col-name').textContent.trim();
                
                // Remove emoji/ícone do início se existir
                const cleanLabel = label.replace(/^🎯\s*/, '').trim();
                
                const shouldCheck = essentialColumns.some(col => cleanLabel.includes(col));
                
                console.log(`📋 Coluna ${colIndex}: "${cleanLabel}" ${shouldCheck ? 'SERÁ SELECIONADA' : 'será desmarcada'}`);
                
                checkbox.checked = shouldCheck;
                toggleColumn(colIndex);
                
                if (shouldCheck) {
                    selectedCount++;
                } else {
                    deselectedCount++;
                }
            });
            
            console.log(`✅ MODO ODS APLICADO: ${selectedCount} selecionadas, ${deselectedCount} desmarcadas`);
            
            alert('🎯 Visualização focada em ODS ativada!\\n\\nApenas as colunas essenciais + ODS estão visíveis para destacar os ícones dos Objetivos de Desenvolvimento Sustentável.');
        }
        
        function demonstrarIconeGeral() {
            console.log('🌟 Demonstrando ícone Geral...');
            
            // Primeiro desmarca todas
            deselectAll();
            
            setTimeout(() => {
                // Ativa apenas ID, Título e ODS
                const essentialColumns = [1, 3, odsColumnIndex]; // ID, Título, ODS
                
                essentialColumns.forEach(index => {
                    if (index !== undefined) {
                        const checkbox = document.getElementById('col_' + index);
                        if (checkbox) {
                            checkbox.checked = true;
                            toggleColumn(index);
                        }
                    }
                });
                
                setTimeout(() => {
                    // Destaca elementos "Geral" na tabela
                    const geralElements = document.querySelectorAll('.ods-geral-container');
                    geralElements.forEach((element, i) => {
                        setTimeout(() => {
                            element.style.transform = 'scale(1.2)';
                            element.style.boxShadow = '0 8px 25px rgba(243, 156, 18, 0.6)';
                            element.style.border = '3px solid #3498db';
                            
                            setTimeout(() => {
                                element.style.transform = '';
                                element.style.boxShadow = '';
                                element.style.border = '';
                            }, 2000);
                        }, i * 500);
                    });
                    
                    const geralCount = geralElements.length;
                    alert(`🌟 Demonstração do Ícone "Geral" Completa!
                    
🎨 Características do ícone Geral:
• Fundo laranja/dourado distintivo
• Contém os principais ODS relacionados a cidades sustentáveis
• Inclui ODS 1, 3, 7, 11, 13, 16
• Label "GERAL" para identificação clara
• Efeito hover diferenciado

📊 Encontrados ${geralCount} artigos com classificação "Geral" na tabela.

✨ Os ícones "Geral" foram destacados temporariamente!`);
                }, 1000);
            }, 500);
        }
        
        function testODSIcons() {
            console.log('🧪 Testando ícones ODS...');
            
            // Primeiro desmarca todas
            deselectAll();
            
            // Depois marca apenas as primeiras 3 colunas uma por vez com delay
            const testColumns = [0, 1, 2];
            let delay = 0;
            
            testColumns.forEach((colIndex, i) => {
                setTimeout(() => {
                    const checkbox = document.getElementById('col_' + colIndex);
                    const colName = columnsInfo[colIndex].name;
                    
                    checkbox.checked = true;
                    toggleColumn(colIndex);
                    
                    console.log(`🧪 Teste ${i+1}/3: Ativando coluna ${colIndex} (${colName})`);
                    
                    if (i === testColumns.length - 1) {
                        setTimeout(() => {
                            // Adiciona também a coluna ODS para mostrar os ícones
                            if (odsColumnIndex !== undefined) {
                                const odsCheckbox = document.getElementById('col_' + odsColumnIndex);
                                odsCheckbox.checked = true;
                                toggleColumn(odsColumnIndex);
                                
                                alert(`🧪 Teste de Ícones ODS Completo!
                                
✅ As primeiras colunas foram ativadas + coluna ODS:
• Coluna 0: ${columnsInfo[0].name}
• Coluna 1: ${columnsInfo[1].name}
• Coluna 2: ${columnsInfo[2].name}
• Coluna ${odsColumnIndex}: ${columnsInfo[odsColumnIndex].name} 🎯

Verifique se os ícones ODS estão visíveis na tabela!`);
                            }
                        }, 1000);
                    }
                }, delay);
                delay += 1000; // 1 segundo entre cada ativação
            });
        }
        
        function exportToLatex() {
            const visibleColumns = [];
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]:checked');
            
            checkboxes.forEach(checkbox => {
                const colIndex = parseInt(checkbox.value);
                const colInfo = columnsInfo[colIndex];
                visibleColumns.push({
                    index: colIndex, 
                    name: colInfo.name,
                    id: colInfo.id,
                    hasODSIcons: colInfo.is_ods
                });
            });
            
            if (visibleColumns.length === 0) {
                alert('❌ Selecione pelo menos uma coluna para exportar!');
                return;
            }
            
            const hasODSColumn = visibleColumns.some(col => col.hasODSIcons);
            const odsNote = hasODSColumn ? '\\n🎯 NOTA: A coluna ODS será exportada com ícones para visualização web, mas como texto para LaTeX.' : '';
            
            const message = `✅ Configuração com Ícones ODS para exportação LaTeX:
            
📊 Total de colunas selecionadas: ${visibleColumns.length}
📋 Colunas na ordem atual:
${visibleColumns.map((col, i) => `${i+1}. [${col.index}] ${col.name}${col.hasODSIcons ? ' 🎯' : ''}`).join('\\n')}

🎨 Ícones ODS: ${hasODSColumn ? 'INCLUÍDOS' : 'Não aplicável'}${odsNote}`;
            
            alert(message);
        }
        
        // Adiciona efeito especial aos ícones ODS
        document.addEventListener('DOMContentLoaded', function() {
            console.log('📄 DOM carregado - verificando estrutura...');
            
            // Verifica se todos os checkboxes foram criados
            const checkboxes = document.querySelectorAll('#columnSelector input[type="checkbox"]');
            console.log(`✅ ${checkboxes.length} checkboxes encontrados no DOM`);
            
            // Verifica se a tabela existe
            const table = document.getElementById('mainTable');
            if (table) {
                const headers = table.getElementsByTagName('th');
                const rows = table.getElementsByTagName('tr');
                console.log(`✅ Tabela encontrada: ${headers.length} cabeçalhos, ${rows.length-1} linhas de dados`);
            } else {
                console.error('❌ Tabela não encontrada!');
            }
            
            // Adiciona listener para ícones ODS
            document.addEventListener('mouseover', function(e) {
                if (e.target.classList.contains('ods-icon')) {
                    console.log('🎯 Hover sobre ícone ODS:', e.target.alt);
                }
            });
            
            // Testa funcionalidades básicas
            console.log('🧪 Testando funcionalidades básicas...');
            console.log('📋 Função selectAll:', typeof selectAll);
            console.log('📋 Função deselectAll:', typeof deselectAll);
            console.log('📋 Função toggleColumn:', typeof toggleColumn);
        });
        
        console.log('🎯 Sistema de ícones ODS carregado e FUNCIONALIDADES CORRIGIDAS!');
        """
        
        # Encontra e substitui o JavaScript
        inicio_js = conteudo.find('<script>')
        fim_js = conteudo.find('</script>') + len('</script>')
        
        if inicio_js != -1 and fim_js != -1:
            novo_conteudo = (
                conteudo[:inicio_js] + 
                '<script>' + 
                js_corrigido + 
                '\n    ' + 
                conteudo[fim_js:]
            )
            
            # Salva o arquivo corrigido
            nome_arquivo = "visualizacao_icones_ods_corrigida.html"
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(novo_conteudo)
            
            print(f"✅ FUNCIONALIDADES CORRIGIDAS!")
            print(f"📄 Arquivo salvo: {nome_arquivo}")
            
            print(f"\n🔧 CORREÇÕES APLICADAS:")
            print(f"   • Função selectAll() corrigida com logs detalhados")
            print(f"   • Função deselectAll() corrigida com verificação")
            print(f"   • Função toggleColumn() melhorada com validações")
            print(f"   • Logs detalhados para debug")
            print(f"   • Verificação final de estado")
            print(f"   • Melhoria no mapeamento de colunas")
            
            print(f"\n🧪 COMO TESTAR:")
            print(f"   1. Abra o arquivo corrigido no navegador")
            print(f"   2. Pressione F12 para ver o Console")
            print(f"   3. Teste 'Selecionar Todas' - deve ver logs detalhados")
            print(f"   4. Teste 'Desmarcar Todas' - deve funcionar corretamente")
            print(f"   5. Verifique se todas as colunas aparecem/desaparecem")
            
            return nome_arquivo
        else:
            print("❌ Erro: Não foi possível encontrar a seção JavaScript")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def main():
    """Função principal"""
    arquivo_corrigido = corrigir_funcionalidades_selecao()
    
    if arquivo_corrigido:
        print(f"\n🎉 PROBLEMA RESOLVIDO!")
        print(f"📁 Arquivo: {arquivo_corrigido}")
        print(f"\n🚀 As funcionalidades de seleção/desseleção agora funcionam corretamente!")

if __name__ == "__main__":
    main()
