#!/bin/bash

echo "🔄 Iniciando processo de build..."

# Verificar se o arquivo principal existe
if [ ! -f "visualizacao_icones_ods_corrigida.html" ]; then
    echo "❌ Erro: arquivo principal não encontrado!"
    exit 1
fi

# Copiar arquivo principal para index.html (GitHub Pages)
echo "📄 Copiando arquivo principal para index.html..."
cp "visualizacao_icones_ods_corrigida.html" "index.html"

# Verificar se os arquivos necessários existem
required_files=(
    "dados_javascript.js"
    "Logo-Estacio-Horizontal-Preto-1-300x101.png"
    "logo-sepado.png"
    "Ícones oficiais - ODS"
    "ícones oficiais - CSC"
)

echo "🔍 Verificando arquivos necessários..."
for file in "${required_files[@]}"; do
    if [ ! -e "$file" ]; then
        echo "⚠️  Aviso: $file não encontrado!"
    else
        echo "✅ $file encontrado"
    fi
done

echo "✅ Build concluído com sucesso!"
echo "📋 Arquivos prontos para deploy:"
echo "   - index.html (arquivo principal)"
echo "   - dados_javascript.js (dados)"
echo "   - Logo-Estacio-Horizontal-Preto-1-300x101.png (logo)"
echo "   - logo-sepado.png (logo)"
echo "   - Ícones oficiais - ODS/ (ícones ODS)"
echo "   - ícones oficiais - CSC/ (ícones CSC)"
