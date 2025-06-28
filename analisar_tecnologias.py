import pandas as pd
import os

# Lê a planilha Excel
file_path = 'Análise de Conteúdo - Luciano 22_06.xlsx'
if os.path.exists(file_path):
    # Lista todas as abas
    xl_file = pd.ExcelFile(file_path)
    print('Abas disponíveis:', xl_file.sheet_names)
    
    # Verifica se existe aba de tecnologias
    tech_sheets = [sheet for sheet in xl_file.sheet_names if 'tecnolog' in sheet.lower() or 'tech' in sheet.lower()]
    print('Abas relacionadas a tecnologia:', tech_sheets)
    
    # Se encontrar aba de tecnologia, analisa as colunas
    if tech_sheets:
        for sheet in tech_sheets:
            df = pd.read_excel(file_path, sheet_name=sheet)
            print(f'\nColunas da aba "{sheet}":')
            for i, col in enumerate(df.columns):
                print(f'  {chr(65+i)} ({i+1}): {col}')
            
            # Mostra algumas linhas da coluna H (índice 7)
            if len(df.columns) > 7:
                col_h = df.columns[7]
                print(f'\nColuna H ({col_h}) - primeiros valores:')
                print(df[col_h].dropna().head(10).tolist())
                
                # Conta frequência das tecnologias
                print(f'\nAnálise de frequência da coluna H:')
                tech_values = df[col_h].dropna()
                
                # Para cada célula, divide por vírgulas e conta
                all_techs = []
                for value in tech_values:
                    if pd.notna(value) and str(value).strip():
                        techs = [tech.strip() for tech in str(value).split(',')]
                        all_techs.extend(techs)
                
                # Conta frequências
                from collections import Counter
                tech_counter = Counter(all_techs)
                print("Top 15 tecnologias mais mencionadas:")
                for tech, count in tech_counter.most_common(15):
                    if tech:  # Remove valores vazios
                        print(f"  {tech}: {count}")
    else:
        print("Nenhuma aba específica de tecnologia encontrada")
        # Analisa todas as abas
        for sheet_name in xl_file.sheet_names:
            print(f'\n=== ABA: {sheet_name} ===')
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f'Colunas:')
            for i, col in enumerate(df.columns):
                print(f'  {chr(65+i)} ({i+1}): {col}')
            
            # Verifica coluna H se existir
            if len(df.columns) > 7:
                col_h = df.columns[7]
                print(f'\nColuna H ({col_h}) - primeiros 5 valores:')
                values = df[col_h].dropna().head(5).tolist()
                for val in values:
                    print(f"  {val}")
else:
    print('Arquivo não encontrado')
