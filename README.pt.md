[🇺🇸 English Version](README.md)

# 📈 Previsão do IPCA com Prophet

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Prophet](https://img.shields.io/badge/Prophet-0066CC?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/Licen%C3%A7a-MIT-blue?style=for-the-badge)

Previsão do índice mensal oficial de inflação do Brasil (IPCA) utilizando Prophet, com e sem variáveis exógenas macroeconômicas, estruturado em 2 níveis progressivos de complexidade.

---

## 📋 Descrição

Este projeto constrói um pipeline completo de previsão de séries temporais para o IPCA (Índice de Preços ao Consumidor Amplo), índice oficial de inflação do Brasil calculado pelo IBGE. O projeto compara duas configurações do Prophet: um modelo sazonal puro (Nível 1) e um modelo enriquecido com variáveis exógenas macroeconômicas (Nível 2).

Todos os dados são coletados em tempo real pela API SGS do Banco Central do Brasil, mantendo cada notebook autocontido, reprodutível e sempre atualizado com o mês mais recente disponível.

---

## 🗂️ Estrutura do Projeto

O projeto é dividido em 2 notebooks, cada um autocontido e reprodutível:

| Notebook | Conteúdo |
|---|---|
| `01_EDA_e_Extracao.ipynb` | Análise Exploratória de Dados: ingestão, análise de distribuição, testes de estacionariedade (ADF/KPSS), ACF/PACF |
| `02_Modelagem_Prophet.ipynb` | Modelagem com Prophet: Nível 1 (puro) e Nível 2 (com variáveis exógenas), além de um apêndice com diagnósticos técnicos |

### Progressão dos Níveis

| Nível | Modelo | Features | Destaques |
|---|---|---|---|
| 1 | Prophet (puro) | Série histórica do IPCA | Baseline estável que captura tendência de longo prazo e sazonalidade anual sem informação externa |
| 2 | Prophet + Regressores | IPCA + SELIC, câmbio, IGP-M | Sensível a mudanças macro; maior alinhamento à trajetória recente da inflação |

---

## 📦 Fontes de Dados

Todos os dados são coletados diretamente da **API SGS do Banco Central do Brasil** em tempo de execução, sem necessidade de arquivos estáticos.

| Variável | Descrição | Código SGS |
|---|---|---|
| IPCA | Índice oficial mensal de inflação do Brasil (IBGE) | 433 |
| SELIC | Taxa básica de juros do Brasil (COPOM) | 4189 |
| Câmbio | Taxa mensal USD/BRL | 3698 |
| IGP-M | Índice Geral de Preços do Mercado (proxy de inflação no atacado) | 189 |

**Período de treino:** Janeiro de 2000 até o final do ano anterior (filtrado para excluir o regime de hiperinflação pré-Plano Real)  
**Período de teste:** ano corrente, atualizado automaticamente conforme novos meses são divulgados

---

## 🛠️ Tecnologias Utilizadas

- Python
- Pandas / NumPy
- Prophet (Meta)
- Scikit-Learn (métricas de avaliação)
- Matplotlib
- Statsmodels (ADF, KPSS, ACF, PACF)
- Requests (API SGS do BCB)

---

## ⚙️ Como Executar

### Pré-requisitos

```bash
pip install pandas numpy matplotlib requests statsmodels prophet scikit-learn
```

### Passos

**Opção A — Executar no Google Colab (recomendado):**

1. Clique no badge abaixo para abrir o notebook principal direto no Colab:

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Marques07/IPCA-Prophet-Forecasting/blob/main/02_Modelagem_Prophet.ipynb)

2. No Colab, vá em **Ambiente de execução → Executar tudo** (ou execute célula por célula)
3. Todas as dependências já vêm instaladas no Colab, exceto o Prophet — o próprio notebook cuida da instalação na primeira célula

**Opção B — Executar localmente:**

1. Clone o repositório:
   ```bash
   git clone https://github.com/Marques07/IPCA-Prophet-Forecasting.git
   ```

2. Abra os notebooks na ordem:
   - Comece com `01_EDA_e_Extracao.ipynb` para contexto
   - Execute `02_Modelagem_Prophet.ipynb` para os modelos Prophet

> **Nota:** A instalação do Prophet pode ser problemática no Windows. O Google Colab é recomendado.

---

## 📊 Resultados e Seleção do Modelo

O Nível 2 (Prophet + variáveis exógenas) supera claramente o Nível 1, tanto visualmente quanto nas métricas de holdout. A previsão do Nível 2 acompanha a trajetória real do IPCA de forma muito mais próxima, especialmente em meses onde as condições macroeconômicas mudam abruptamente.

A razão é direta: as variáveis exógenas dão ao modelo um contexto que o padrão sazonal sozinho não consegue fornecer. Quando SELIC, câmbio e IGP-M se movem, eles carregam informação sobre para onde a inflação está indo. O Nível 1 só vê o calendário; o Nível 2 vê o calendário *e* o ambiente macro.

Uma ressalva: o `add_regressor` do Prophet assume que as variáveis exógenas afetam a inflação imediatamente, enquanto na realidade a SELIC transmite com defasagem de 6 a 12 meses. Mesmo com essa simplificação, o contexto adicional faz uma diferença clara.

> **Nota importante de interpretação:** a previsão do Nível 2 utiliza os valores *reais* de SELIC, câmbio e IGP-M durante o período de teste — não previsões. Isso significa que o Nível 2 responde à pergunta "dado o que sabemos sobre o ambiente macro, qual deveria ser o IPCA?" em vez de "qual será o IPCA, sem nenhuma informação futura?". Este é um setup comum e válido para previsão condicional.

> **Achado principal sobre retreino:** uma validação walk-forward (disponível no apêndice do notebook) mostrou apenas melhoria modesta em relação ao modelo congelado. Isso sugere que, para este conjunto de dados, adicionar informação exógena (Nível 2) gera um ganho preditivo maior do que retreinar periodicamente com mais dados históricos.

---

## 🔮 Previsão em Tempo Real

Ambos os notebooks incluem uma seção de **Previsão em Tempo Real** que gera automaticamente uma previsão para o próximo mês do IPCA ainda não divulgado. Assim que o IBGE publicar o valor oficial, a previsão pode ser comparada com o resultado real para validar o modelo em um cenário do mundo real.

---

## 🔬 Apêndice — Diagnósticos Técnicos

O notebook do Prophet inclui um apêndice com diagnósticos suplementares, mantidos separados do pipeline principal:

1. **Decomposição de Componentes do Prophet** — como o modelo divide a série do IPCA em tendência e sazonalidade anual
2. **Validação Cruzada Temporal** — validação cruzada nativa do Prophet em múltiplas janelas históricas (Nível 1 e Nível 2)
3. **Walk-Forward Validation** — comparação entre um modelo congelado e um modelo retreinado periodicamente, simulando um pipeline de produção

---

## ⚠️ Limitações

- **Janela de holdout dinâmica:** o conjunto de teste é o ano corrente até a data atual, então cresce conforme novos meses são divulgados. Isso reflete o uso no mundo real, mas significa que as métricas evoluem mês a mês em vez de serem diretamente comparáveis entre execuções.
- **Premissa de efeito instantâneo dos regressores:** o `add_regressor` trata cada variável exógena como tendo efeito contemporâneo sobre o IPCA. Na prática, variáveis como a SELIC transmitem com defasagem de 6 a 12 meses, então o modelo captura apenas parte da cadeia causal. Essa é uma simplificação conhecida do Prophet, não um bug.
- **Sem persistência de modelo:** o modelo é retreinado a cada execução. Isso mantém o notebook totalmente autocontido e reprodutível, mas precisaria ser adaptado para um deployment em produção, onde artefatos de modelo são versionados e armazenados em cache.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
