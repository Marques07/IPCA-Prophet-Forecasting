[🇺🇸 English Version](README.md)

# 📈 Previsão do IPCA com Prophet

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Prophet](https://img.shields.io/badge/Prophet-0066CC?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

Previsão do índice de inflação oficial mensal do Brasil (IPCA) usando Prophet, com e sem variáveis exógenas macroeconômicas, estruturado em 2 níveis progressivos de complexidade.

---

## 📋 Descrição

Este projeto constrói um pipeline completo de previsão de séries temporais para o IPCA (Índice Nacional de Preços ao Consumidor Amplo), o índice de inflação oficial do Brasil calculado pelo IBGE. O projeto compara duas configurações do Prophet: um modelo sazonal puro (Nível 1) e um modelo enriquecido com variáveis exógenas macroeconômicas (Nível 2).

Todos os dados são extraídos em tempo real da API SGS do Banco Central do Brasil, mantendo cada notebook autossuficiente, reprodutível e sempre atualizado com o mês mais recente disponível. Todo o pipeline é **automatizado via GitHub Actions** (veja abaixo).

---

## 🗂️ Estrutura do Projeto

O projeto está dividido em 2 notebooks, cada um autossuficiente e reprodutível:

| Notebook | Conteúdo |
|---|---|
| `01_EDA_e_Extracao.ipynb` | Análise Exploratória de Dados: ingestão de dados, análise de distribuição, testes de estacionariedade (ADF/KPSS), ACF/PACF |
| `02_Modelagem_Prophet.ipynb` | Modelagem com Prophet: Nível 1 (puro) e Nível 2 (com variáveis exógenas), além de um apêndice com diagnósticos técnicos |

### Progressão de Níveis

| Nível | Modelo | Features | Destaques |
|---|---|---|---|
| 1 | Prophet (puro) | Série histórica do IPCA | Baseline estável que captura tendência de longo prazo e sazonalidade anual sem insumos externos |
| 2 | Prophet + Regressores | IPCA + SELIC, câmbio, IGP-M | Sensível a mudanças macro; alinha-se mais de perto com a trajetória recente da inflação |

---

## 📦 Fontes de Dados

Todos os dados são buscados diretamente da **API SGS do Banco Central do Brasil** em tempo de execução, sem a necessidade de arquivos estáticos.

| Variável | Descrição | Código SGS |
|---|---|---|
| IPCA | Índice de inflação oficial mensal do Brasil (IBGE) | 433 |
| SELIC | Taxa de juros básica do Brasil (COPOM) | 4189 |
| Câmbio | Taxa mensal USD/BRL | 3698 |
| IGP-M | Índice Geral de Preços do Mercado (proxy de inflação no atacado) | 189 |

**Período de treinamento:** Janeiro de 2000 até o final do ano anterior (filtrado para excluir o regime de hiperinflação pré-Plano Real)  
**Período de Holdout (teste):** ano corrente, atualizado automaticamente conforme novos meses são divulgados

---

## 🛠️ Construído Com

- Python
- Pandas / NumPy
- Prophet (Meta)
- Scikit-Learn (métricas de avaliação)
- Matplotlib
- Statsmodels (ADF, KPSS, ACF, PACF)
- Requests (API SGS do BCB)

---

## 🤖 Automação (GitHub Actions)

Este repositório conta com um pipeline completo de CI/CD via GitHub Actions. No 1º dia de cada mês, um workflow automaticamente:

1. Instala as dependências.
2. Executa ambos os notebooks usando `papermill` (buscando os dados mais recentes da API do BCB).
3. Limpa o estado de widgets específicos do Colab para manter o histórico do git limpo.
4. Faz o commit e push dos notebooks atualizados com as novas previsões.

---

## ⚙️ Como Executar

### Pré-requisitos

```bash
pip install pandas numpy matplotlib requests statsmodels prophet scikit-learn
```

### Passos

**Opção A — Executar no Colab (recomendado):**

| Notebook | Abrir no Colab |
|---|---|
| 1. Análise Exploratória de Dados | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Marques07/IPCA-Prophet-Forecasting/blob/main/01_EDA_e_Extracao.ipynb) |
| 2. Modelagem com Prophet | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Marques07/IPCA-Prophet-Forecasting/blob/main/02_Modelagem_Prophet.ipynb) |

1. No Colab, vá em **Runtime → Run all** (ou execute as células manualmente).
2. Todas as dependências já estão pré-instaladas no Colab, exceto o Prophet — o notebook lida com a instalação na primeira célula.

**Opção B — Executar localmente:**

1. Clone o repositório:
   ```bash
   git clone https://github.com/Marques07/IPCA-Prophet-Forecasting.git
   ```
2. Abra os notebooks na ordem:
   - Comece com `01_EDA_e_Extracao.ipynb` para contexto.
   - Execute `02_Modelagem_Prophet.ipynb` para os modelos Prophet.

> **Nota:** A instalação do Prophet pode ser complicada no Windows. O Google Colab é recomendado.

---

## 📊 Resultados e Seleção do Modelo

O Nível 2 (Prophet + variáveis exógenas) supera claramente o Nível 1, tanto visualmente quanto nas métricas do holdout. A previsão do Nível 2 acompanha a trajetória real do IPCA muito mais de perto, especialmente durante meses em que as condições macroeconômicas mudam abruptamente.

A razão é direta: as variáveis exógenas dão ao modelo um contexto que o padrão sazonal isolado não consegue fornecer. Quando SELIC, câmbio e IGP-M se movem, eles carregam informações sobre para onde a inflação está indo. O Nível 1 só enxerga o calendário; o Nível 2 enxerga o calendário *e* o ambiente macro.

Uma ressalva: o `add_regressor` do Prophet assume que as variáveis exógenas afetam a inflação imediatamente, enquanto na realidade a SELIC transmite com um lag de 6 a 12 meses. Mesmo com essa simplificação, o contexto adicionado faz uma diferença clara.

> **Nota importante sobre a interpretação:** a previsão do Nível 2 usa os valores reais de SELIC, câmbio e IGP-M durante o período de teste — não previsões. Isso significa que o Nível 2 responde à pergunta "dado o que sabemos sobre o ambiente macro, qual deveria ser o IPCA?" em vez de "qual será o IPCA, sem qualquer informação futura?". Esta é uma configuração comum e válida para previsão condicional.

---

## 🔮 Previsão em Tempo Real (Live Forecast)

Ambos os notebooks incluem uma seção de Live Forecast que gera automaticamente uma previsão para o próximo mês do IPCA ainda não divulgado. Assim que o IBGE publicar o número oficial, a previsão poderá ser comparada com o resultado para validar o modelo em um cenário do mundo real.

---

## 🔬 Apêndice — Validação Walk-Forward

O notebook do Prophet inclui um apêndice focado na Validação Walk-Forward. Como as variáveis exógenas (SELIC, câmbio, IGP-M) não podem ser perfeitamente previstas para horizontes de múltiplos passos à frente sem adicionar incerteza significativa, a validação cruzada tradicional para o Nível 2 não é empregada aqui.

Em vez disso, a validação walk-forward atua como o teste mais honesto e robusto:

1. **Decomposição de Componentes do Prophet** — visualiza a tendência e a sazonalidade anual.
2. **Validação Walk-Forward (Nível 1)** — uma simulação de retreinamento incremental (mês a mês ao longo dos últimos 24 meses) para medir como o modelo Prophet puro se comporta em um pipeline similar ao de produção.

---

## ⚠️ Limitações

- **A janela do Holdout é dinâmica:** o conjunto de teste é o ano corrente até a data atual, portanto cresce conforme novos meses são divulgados. Isso espelha o uso no mundo real, mas significa que as métricas evoluem mês a mês em vez de serem diretamente comparáveis entre execuções.
- **Premissa de regressor instantâneo:** `add_regressor` trata cada variável exógena como tendo um efeito contemporâneo sobre o IPCA. Na prática, variáveis como a SELIC transmitem com um lag de 6 a 12 meses, então o modelo captura apenas parte da cadeia causal. Esta é uma simplificação conhecida do Prophet, não um bug.
- **Escopo do Walk-forward:** a validação walk-forward aplica-se apenas ao Nível 1 (Prophet puro). Retreinar o Nível 2 mês a mês exigiria prever as variáveis exógenas em cada etapa, o que está fora do escopo deste projeto. A comparação entre o holdout congelado e o walk-forward é indicativa, não perfeitamente comparável (apples-to-apples).
- **Sem persistência de modelo:** o modelo é retreinado a cada execução. Isso mantém o notebook totalmente autossuficiente e reprodutível, mas precisaria ser adaptado para uma implantação em produção onde os artefatos do modelo são versionados e armazenados em cache.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
