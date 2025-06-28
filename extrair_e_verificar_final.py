from docx import Document
import re

def extrair_e_verificar_correcoes():
    """
    Extrai texto do documento DOCX corrigido e verifica se as correções foram aplicadas
    """
    
    import glob
    docx_files = glob.glob('*.docx')
    if not docx_files:
        print("❌ Nenhum arquivo DOCX encontrado")
        return False
    
    # Usar o documento principal (não o backup)
    docx_path = [f for f in docx_files if 'BACKUP' not in f][0]
    print(f"📄 Verificando documento: {docx_path}")
    
    try:
        doc = Document(docx_path)
        
        # Extrair texto da seção 4.2
        secao_42_iniciada = False
        paragrafos_secao = []
        
        for i, para in enumerate(doc.paragraphs):
            texto = para.text.strip()
            
            if re.match(r'4\.2\s+RESULTADOS', texto, re.IGNORECASE):
                secao_42_iniciada = True
                print(f"✅ Seção 4.2 encontrada no parágrafo {i}")
            
            if secao_42_iniciada and re.match(r'5\.\d+|CAPÍTULO\s+5|5\s+DISCUSSÃO', texto, re.IGNORECASE):
                print(f"🔚 Fim da seção 4.2 no parágrafo {i}")
                break
            
            if secao_42_iniciada and texto:
                paragrafos_secao.append(f"[P{i}] {texto}")
        
        # Salvar texto extraído
        texto_completo = '\n\n'.join(paragrafos_secao)
        with open('4.2 RESULTADOS DA ANÁLISE DE CONTEÚ.txt', 'w', encoding='utf-8') as f:
            f.write(texto_completo)
        
        print(f"💾 Seção 4.2 atualizada salva com {len(paragrafos_secao)} parágrafos")
        
        # Verificar especificamente as correções dos pilares
        print("\\n🔍 VERIFICANDO CORREÇÕES DOS PILARES CSC...")
        
        correções_encontradas = {
            'mobilidade_92_7': False,
            'tecnologia_92_7': False,
            'governanca_90_2': False,
            'energia_82_9': False,
            'meio_ambiente_80_5': False,
            'urbanismo_56_1': False
        }
        
        for para in paragrafos_secao:
            texto_lower = para.lower()
            
            if 'mobilidade (38 menções, 92,7%' in texto_lower or 'mobilidade (38 menções, 92.7%' in texto_lower:
                correções_encontradas['mobilidade_92_7'] = True
                print("✅ Mobilidade corrigida para 92,7%")
            
            if 'tecnologia e inovação (38 menções, 92,7%' in texto_lower or 'tecnologia e inovação (38 menções, 92.7%' in texto_lower:
                correções_encontradas['tecnologia_92_7'] = True
                print("✅ Tecnologia e Inovação corrigida para 92,7%")
            
            if 'governança (37 menções, 90,2%' in texto_lower or 'governança (37 menções, 90.2%' in texto_lower:
                correções_encontradas['governanca_90_2'] = True
                print("✅ Governança corrigida para 90,2%")
            
            if 'energia (34 menções, 82,9%' in texto_lower or 'energia (34 menções, 82.9%' in texto_lower:
                correções_encontradas['energia_82_9'] = True
                print("✅ Energia corrigida para 82,9%")
            
            if 'meio ambiente (33 menções, 80,5%' in texto_lower or 'meio ambiente (33 menções, 80.5%' in texto_lower:
                correções_encontradas['meio_ambiente_80_5'] = True
                print("✅ Meio Ambiente corrigido para 80,5%")
            
            if 'urbanismo (23 menções, 56,1%' in texto_lower or 'urbanismo (23 menções, 56.1%' in texto_lower:
                correções_encontradas['urbanismo_56_1'] = True
                print("✅ Urbanismo corrigido para 56,1%")
        
        # Resumo das correções
        total_correções = sum(correções_encontradas.values())
        print(f"\\n📊 RESUMO DAS CORREÇÕES:")
        print(f"   ✅ Correções aplicadas: {total_correções}/6")
        
        if total_correções == 6:
            print("🎉 TODAS as correções dos pilares CSC foram aplicadas com sucesso!")
        else:
            print("⚠️ Algumas correções ainda não foram aplicadas:")
            for correcao, aplicada in correções_encontradas.items():
                if not aplicada:
                    print(f"   ❌ {correcao}")
        
        return total_correções == 6
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    sucesso = extrair_e_verificar_correcoes()
    
    if sucesso:
        print("\\n🎯 EXECUTANDO AUDITORIA FINAL...")
        
        # Executar auditoria com o arquivo atualizado
        import subprocess
        try:
            resultado = subprocess.run([
                "c:/Users/lucia/Dissertação/.venv/Scripts/python.exe", 
                "auditoria_dados_dissertacao.py"
            ], capture_output=True, text=True, cwd=".")
            
            print("📋 RESULTADO DA AUDITORIA FINAL:")
            linhas = resultado.stdout.split('\\n')
            for linha in linhas[-20:]:  # Últimas 20 linhas
                if linha.strip():
                    print(linha)
                    
        except Exception as e:
            print(f"⚠️ Erro na auditoria: {e}")
    else:
        print("❌ Nem todas as correções foram aplicadas. Verificação manual necessária.")
