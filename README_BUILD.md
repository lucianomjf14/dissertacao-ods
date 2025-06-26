# 🎓 Dissertação ODS - Visualização Interativa

## 📊 Sobre o Projeto

Aplicação web interativa para visualização dos dados da dissertação **"Cidades Inteligentes como Vetores para os ODS"** de Luciano Marinho Silveira, do Mestrado em Administração e Desenvolvimento Empresarial da Universidade Estácio de Sá.

🌐 **Demo ao vivo:** https://lucianomjf14.github.io/dissertacao-ods/

## 🚀 Características

- ✅ **Visualização interativa** de dados dos ODS (Objetivos de Desenvolvimento Sustentável)
- ✅ **Sistema de filtros** por categorias (Metadados, Tecnologias, ODS, CSC)
- ✅ **Truncamento inteligente** de textos longos com botão "Ver mais/Ver menos"
- ✅ **Links clicáveis** para acesso direto aos artigos
- ✅ **Ícones visuais** dos ODS e pilares CSC (Cidades Sustentáveis e Conectadas)
- ✅ **Responsivo** e otimizado para diferentes dispositivos
- ✅ **Deploy automático** via GitHub Pages

## 🛠️ Tecnologias Utilizadas

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Estilização:** TailwindCSS
- **Gráficos:** Chart.js
- **Deploy:** GitHub Pages
- **CI/CD:** GitHub Actions

## 📁 Estrutura do Projeto

```
├── index.html                          # Arquivo principal da aplicação
├── dados_javascript.js                 # Dados da pesquisa
├── visualizacao_icones_ods_corrigida.html # Arquivo fonte
├── package.json                        # Configurações do projeto
├── build.ps1                          # Script de build (PowerShell)
├── build.sh                           # Script de build (Bash)
├── .github/workflows/deploy.yml       # GitHub Actions
├── Logo-Estacio-Horizontal-Preto-1-300x101.png
├── logo-sepado.png
├── Ícones oficiais - ODS/             # Ícones dos ODS
└── ícones oficiais - CSC/             # Ícones dos pilares CSC
```

## 🔧 Processo de Build

### Método 1: Scripts Automatizados

#### Windows (PowerShell):
```powershell
.\build.ps1
```

#### Linux/Mac (Bash):
```bash
./build.sh
```

### Método 2: NPM Scripts

```bash
# Build
npm run build

# Desenvolvimento local
npm run dev

# Build + Deploy
npm run deploy
```

### Método 3: Manual

1. Copiar `visualizacao_icones_ods_corrigida.html` para `index.html`
2. Verificar se todos os arquivos estão presentes
3. Fazer commit e push

## 🚀 Deploy

O deploy é feito automaticamente via **GitHub Actions** quando há push na branch `master`.

### Deploy Manual:
```bash
git add .
git commit -m "Deploy: Atualização da aplicação"
git push origin master
```

## 📋 Funcionalidades

### 🔍 Filtros de Visualização
- **Todas:** Mostra todas as colunas com truncamento inteligente
- **Metadados:** ID, Link, Autores, Título, Ano, Periódico, etc.
- **Tecnologias:** Palavras-chave, categorias, aspectos principais
- **ODS:** Foco nos Objetivos de Desenvolvimento Sustentável
- **CSC:** Indicadores e pilares das Cidades Sustentáveis e Conectadas

### 📊 Métricas dos ODS
- Visualização em cards dos ODS mais mencionados
- Contagem automática por artigo
- Ícones oficiais da ONU

### 🔗 Links Interativos
- Links diretos para os artigos científicos
- Abertura em nova aba para não perder o contexto
- Visual destacado para fácil identificação

## 🎨 Design

- **Paleta de cores:** Azul corporativo da Estácio
- **Tipografia:** Inter (Google Fonts)
- **Layout:** Responsivo com Grid CSS
- **Animações:** Suaves e profissionais
- **UX:** Intuitivo e acessível

## 📝 Como Atualizar os Dados

1. Modificar `dados_javascript.js` com novos dados
2. Executar `.\build.ps1` (Windows) ou `./build.sh` (Linux/Mac)
3. Fazer commit e push
4. GitHub Pages atualizará automaticamente em ~2 minutos

## 👨‍🎓 Autor

**Luciano Marinho Silveira**  
Mestrado em Administração e Desenvolvimento Empresarial  
Universidade Estácio de Sá - UNESA

---

⭐ **Link da Aplicação:** https://lucianomjf14.github.io/dissertacao-ods/
