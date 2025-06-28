#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar valores ODS e criar visualização com ícones
"""

import pandas as pd
from pathlib import Path

def analisar_valores_ods():
    """Analisa os valores da coluna ODS"""
    df = pd.read_excel('Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx')
    print('Valores únicos na coluna ODS:')
    valores_ods = df['ODS (Geral / Específico)'].dropna().unique()
    for valor in sorted(valores_ods):
        print(f'  - "{valor}"')
    return df

if __name__ == "__main__":
    analisar_valores_ods()
