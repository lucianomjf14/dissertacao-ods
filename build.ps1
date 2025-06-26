# Script de Build para GitHub Pages
# Uso: .\build.ps1

Write-Host "🔄 Iniciando processo de build..." -ForegroundColor Cyan

# Verificar se o arquivo principal existe
if (-not (Test-Path "visualizacao_icones_ods_corrigida.html")) {
    Write-Host "❌ Erro: arquivo principal não encontrado!" -ForegroundColor Red
    exit 1
}

# Copiar arquivo principal para index.html (GitHub Pages)
Write-Host "📄 Copiando arquivo principal para index.html..." -ForegroundColor Yellow
Copy-Item "visualizacao_icones_ods_corrigida.html" "index.html" -Force

# Verificar se os arquivos necessários existem
$requiredFiles = @(
    "dados_javascript.js",
    "Logo-Estacio-Horizontal-Preto-1-300x101.png",
    "logo-sepado.png",
    "Ícones oficiais - ODS",
    "ícones oficiais - CSC"
)

Write-Host "🔍 Verificando arquivos necessários..." -ForegroundColor Yellow
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file encontrado" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Aviso: $file não encontrado!" -ForegroundColor Yellow
    }
}

Write-Host "✅ Build concluído com sucesso!" -ForegroundColor Green
Write-Host "📋 Arquivos prontos para deploy:" -ForegroundColor Cyan
Write-Host "   - index.html (arquivo principal)" -ForegroundColor White
Write-Host "   - dados_javascript.js (dados)" -ForegroundColor White
Write-Host "   - Logo-Estacao-Horizontal-Preto-1-300x101.png (logo)" -ForegroundColor White
Write-Host "   - logo-sepado.png (logo)" -ForegroundColor White
Write-Host "   - Ícones oficiais - ODS/ (ícones ODS)" -ForegroundColor White
Write-Host "   - ícones oficiais - CSC/ (ícones CSC)" -ForegroundColor White

Write-Host "`n🚀 Para fazer deploy:" -ForegroundColor Cyan
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Deploy: Atualização da aplicação'" -ForegroundColor Gray
Write-Host "   git push origin master" -ForegroundColor Gray
