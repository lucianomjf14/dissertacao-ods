# INSTRUÇÕES PARA IMPLEMENTAR A TABELA ABNT NA DISSERTAÇÃO

## Arquivos Criados

1. **tabela_abnt_final.tex** - Versão final recomendada (formato longitudinal)
2. **tabela_apendice_compacta.tex** - Versão compacta (formato paisagem)
3. **tabela_apendice_longitudinal.tex** - Versão longitudinal (formato retrato)
4. **tabela_abnt.tex** - Versão original simples

## Versão Recomendada: tabela_abnt_final.tex

### Por que esta versão é recomendada:
- ✅ Segue rigorosamente as normas ABNT
- ✅ Quebra automaticamente entre páginas
- ✅ Mantém cabeçalho repetido em todas as páginas
- ✅ Inclui "Continuação da página anterior" e "Continua na próxima página"
- ✅ Formatação adequada para dissertações de mestrado
- ✅ Títulos completos dos artigos (não truncados)

## Como Implementar

### 1. Pacotes Necessários no Preâmbulo

Adicione no preâmbulo do seu documento LaTeX:

```latex
\usepackage{longtable}
\usepackage{array}
\usepackage[brazil]{babel}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{a4paper, margin=2.5cm}
```

### 2. No Apêndice da Dissertação

```latex
\appendix

\chapter{CORPUS DA ANÁLISE DE CONTEÚDO}
\label{apendice:corpus}

Este apêndice apresenta o corpus completo da análise de conteúdo realizada 
nesta pesquisa, constituído por 41 artigos científicos selecionados conforme 
os critérios de inclusão e exclusão estabelecidos na metodologia. Os artigos 
abrangem o período de 2020 a 2024, demonstrando a relevância contemporânea 
do tema de cidades inteligentes sustentáveis.

% Insira aqui o conteúdo do arquivo tabela_abnt_final.tex
\input{tabela_abnt_final.tex}
```

### 3. Como Referenciar no Texto

```latex
O corpus da pesquisa foi constituído por 41 artigos científicos selecionados 
conforme os critérios de inclusão e exclusão estabelecidos na metodologia, 
conforme apresentado na Tabela \ref{tab:corpus_analise_conteudo} (Apêndice 
\ref{apendice:corpus}).
```

## Características da Tabela Criada

### Estrutura
- **Colunas**: ID, Autores, Título, Ano, Periódico
- **Linhas**: 41 artigos do corpus
- **Período**: 2020-2024
- **Formatação**: Conforme normas ABNT

### Recursos ABNT Implementados
- ✅ Título centralizado e numerado
- ✅ Label para referência cruzada
- ✅ Fonte indicada no rodapé
- ✅ Linhas de separação adequadas
- ✅ Formatação de texto apropriada
- ✅ Quebra de página automática

## Alternativas Caso Necessite Modificações

### Opção 1: Tabela Compacta (Paisagem)
- Use `tabela_apendice_compacta.tex`
- Inclua `\usepackage{rotating}` no preâmbulo
- Coloque a tabela dentro de `\begin{landscape}...\end{landscape}`

### Opção 2: Personalizar Colunas
Se quiser incluir outras colunas (como ODS, Aspectos Principais), 
use `tabela_apendice_compacta.tex` como base e ajuste conforme necessário.

## Dicas de Formatação

### Para Melhor Aparência
1. **Espaçamento**: A tabela já inclui espaçamento adequado
2. **Fonte**: Mantenha o `\footnotesize` para caber melhor na página
3. **Alinhamento**: Textos estão alinhados à esquerda conforme ABNT

### Compilação
1. Use `pdflatex` para compilar
2. Compile pelo menos 2 vezes para resolver as referências
3. Se usar `bibtex`, compile na ordem: latex → bibtex → latex → latex

## Dados da Tabela

- **Total de artigos**: 41
- **Período coberto**: 2020-2024
- **Principais periódicos**: Sustainability, Smart Cities, Applied Sciences
- **Foco temático**: Cidades inteligentes sustentáveis e ODS

## Resolução de Problemas Comuns

### Se a tabela não compilar:
1. Verifique se todos os pacotes estão instalados
2. Certifique-se de que o arquivo .tex está no mesmo diretório
3. Verifique se há caracteres especiais não escapados

### Se a tabela ficar muito larga:
1. Use a versão longitudinal (recomendada)
2. Ou use a versão paisagem com `\begin{landscape}`

### Se quiser modificar o conteúdo:
1. Os scripts Python estão disponíveis para regenerar a tabela
2. Modifique o arquivo Excel e execute novamente o script

## Contato

Se tiver dúvidas sobre a implementação, pode consultar:
- Manual ABNT NBR 14724 (Trabalhos acadêmicos)
- Documentação do pacote `longtable`
- Guias de LaTeX para dissertações

---

**Observação**: Esta tabela foi gerada automaticamente a partir do arquivo Excel 
`Analise_de_Conteudo_Com_Corpus_Corrigido.xlsx` e formatada conforme as normas ABNT 
para dissertações de mestrado.
