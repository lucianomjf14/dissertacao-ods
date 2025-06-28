import pandas as pd
from collections import Counter

# Lê a aba de tecnologias
df = pd.read_excel('Análise de Conteúdo - Luciano 22_06.xlsx', sheet_name='Tecnologias')

# Analisa a coluna H (Tecnologias)
tech_column = df['Tecnologias']
total_studies = len(df)

# Processa todas as tecnologias
all_techs = []
study_tech_mapping = {}

for idx, value in enumerate(tech_column):
    study_id = df.iloc[idx]['ID']
    if pd.notna(value) and str(value).strip() and str(value).strip() != '-':
        techs = [tech.strip() for tech in str(value).split(',')]
        all_techs.extend(techs)
        study_tech_mapping[study_id] = techs
    else:
        study_tech_mapping[study_id] = []

# Conta frequências
tech_counter = Counter(all_techs)

# Remove valores vazios e '-'
tech_counter_filtered = {k: v for k, v in tech_counter.items() if k and k != '-'}
tech_counter = Counter(tech_counter_filtered)

# Calcula estatísticas
total_mentions = sum(tech_counter.values())
studies_with_tech = len([v for v in study_tech_mapping.values() if v])

print(f"=== ESTATÍSTICAS DAS TECNOLOGIAS ===")
print(f"Total de estudos: {total_studies}")
print(f"Estudos com tecnologias identificadas: {studies_with_tech}")
print(f"Estudos sem tecnologias identificadas: {total_studies - studies_with_tech}")
print(f"Total de menções de tecnologias: {total_mentions}")
print(f"Tecnologias únicas identificadas: {len(tech_counter)}")
print(f"Média de tecnologias por estudo: {total_mentions / total_studies:.1f}")

print(f"\n=== RANKING DAS TECNOLOGIAS ===")
for tech, count in tech_counter.most_common():
    percentage = (count / total_studies) * 100
    print(f"{tech}: {count} estudos ({percentage:.1f}%)")

# Gera dados JavaScript para a visualização
print(f"\n=== DADOS PARA JAVASCRIPT ===")
print("const validatedTechData = {")
for tech, count in tech_counter.most_common():
    percentage = (count / total_studies) * 100
    tech_clean = tech.replace('"', '\\"')
    print(f'    "{tech_clean}": {{ name: "{tech_clean}", studiesCount: {count}, count: {count}, percentage: {percentage:.1f} }},')

# Para tecnologias não mencionadas (se houver uma lista padrão)
print('};')

print(f"\nTotal de estudos para cálculo: {total_studies}")
