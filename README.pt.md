[🇺🇸 English Version](README.md)

# 📈 Previsão do IPCA — Prophet vs XGBoost

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Prophet](https://img.shields.io/badge/Prophet-0066CC?style=for-the-badge&logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-EA4335?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/Licença-MIT-blue?style=for-the-badge)

Previsão do índice mensal oficial de inflação do Brasil (IPCA) utilizando Prophet e XGBoost, com e sem variáveis exógenas macroeconômicas, estruturado em 4 níveis progressivos de complexidade.

---

## 📋 Descrição

Este projeto constrói um pipeline completo de previsão de séries temporais para o IPCA (Índice de Preços ao Consumidor Amplo), índice oficial de inflação do Brasil calculado pelo IBGE. O projeto compara duas abordagens de modelagem fundamentalmente diferentes: um modelo baseado em decomposição (Prophet) e um modelo de gradient boosting (XGBoost), em múltiplos níveis de complexidade, com e sem variáveis macroeconômicas.

Todos os dados são coletados em tempo real pela API SGS do Banco Central do Brasil, mantendo cada notebook autocontido, reprodutível e sempre atualizado com o mês mais recente disponível.

---

## 🗂️ Estrutura do Projeto

O projeto é dividido em 3 notebooks, cada um autocontido e reprodutível:

| Notebook | Conteúdo |
|---|---|
| `01_EDA_e_Extracao.ipynb` | Análise Exploratória de Dados: ingestão, análise de distribuição, testes de estacionariedade (ADF/KPSS), ACF/PACF |
| `02_Modelagem_Prophet.ipynb` | Níveis 1 e 2: Prophet sem e com variáveis exógenas |
| `03_XGBoost_Modelagem.ipynb` | Níveis 3 e 4: XGBoost sem e com variáveis exógenas |

### Progressão dos Níveis

| Nível | Modelo | Features | Destaques |
|---|---|---|---|
| 1 | Prophet (puro) | Série histórica do IPCA | Baseline estável que captura tendência de longo prazo e sazonalidade anual |
| 2 | Prophet + Regressores | IPCA + SELIC, câmbio, IGP-M | Sensível a mudanças macro com maior alinhamento à trajetória recente da inflação |
| 3 | XGBoost (puro) | Lags do IPCA + features de calendário | Melhor MAE agregado impulsionado pela forte estrutura de autocorrelação AR(1) |
| 4 | XGBoost + Exógenas | Lags do IPCA + variáveis macro defasadas | Viés de reversão à média onde as variáveis macro diluem o sinal dos lags |

---

## 📦 Fontes de Dados

Todos os dados são coletados diretamente da **API SGS do Banco Central do Brasil** em tempo de execução, sem necessidade de arquivos estáticos.

| Variável | Descrição | Código SGS |
|---|---|---|
| IPCA | Índice oficial mensal de inflação do Brasil (IBGE) | 433 |
| SELIC | Taxa básica de juros do Brasil (COPOM) | 4189 |
| Câmbio | Taxa mensal USD/BRL | 3698 |
| IGP-M | Índice Geral de Preços do Mercado (proxy de inflação no atacado) | 189 |

**Período de treino:** Janeiro de 2000 a Dezembro de 2025  
**Período de teste:** Janeiro de 2026 em diante, atualizado automaticamente conforme novos meses são divulgados

---

## 🛠️ Tecnologias Utilizadas

- Python
- Pandas / NumPy
- Prophet (Meta)
- XGBoost
- Scikit-Learn (`RandomizedSearchCV`, `TimeSeriesSplit`)
- Matplotlib
- Statsmodels
- Requests (API SGS do BCB)

---

## ⚙️ Como Executar

### Pré-requisitos

```bash
pip install pandas numpy matplotlib requests statsmodels prophet xgboost scikit-learn
```

### Passos

1. Clone o repositório
```bash
git clone https://github.com/Marques07/IPCA-Prophet-vs-XGBoost.git
```

2. Abra os notebooks na ordem:
   - Comece com `01_EDA_e_Extracao.ipynb` para contexto
   - Execute `02_Modelagem_Prophet.ipynb` para os modelos Prophet (recomendado: Google Colab)
   - Execute `03_XGBoost_Modelagem.ipynb` para os modelos XGBoost (VS Code ou Jupyter)

> **Nota:** A instalação do Prophet pode ser problemática no Windows. O Google Colab é recomendado para o notebook do Prophet.

---

## 📊 Resultados e Seleção do Modelo

O MAE agregado ao longo do holdout de 2026 favorece o XGBoost puro, impulsionado pela forte estrutura AR(1) da série do IPCA. No entanto, as métricas agregadas por si só não contam a história completa.

O Prophet com variáveis exógenas demonstrou precisão crescente conforme mais meses de 2026 foram sendo disponibilizados, capturando a trajetória da inflação de forma mais próxima nos meses recentes. Para o propósito de previsão do próximo mês, onde o alinhamento com a tendência recente importa mais do que o erro médio histórico, o Prophet com regressores demonstrou comportamento preditivo mais robusto no mundo real.

O XGBoost puro permanece o modelo mais consistente no agregado, mas suas previsões mostram menor sensibilidade às condições macroeconômicas atuais. O XGBoost com variáveis exógenas exibe viés de reversão à média, convergindo para a média histórica independentemente da variação dos inputs.

> As métricas são recalculadas automaticamente a cada execução conforme novos meses ficam disponíveis. Consulte os outputs dos notebooks para os valores atuais de MAE e RMSE.

---

## 🔮 Previsão em Tempo Real

Ambos os notebooks incluem uma seção de **Previsão em Tempo Real** que gera automaticamente uma previsão para o próximo mês do IPCA ainda não divulgado. Assim que o IBGE publicar o valor oficial, a previsão pode ser comparada com o resultado real para validar os modelos em um cenário do mundo real.

---

## ⚠️ Limitações

- A janela de holdout cresce automaticamente conforme novos meses são divulgados, então as métricas melhoram com o tempo
- O `add_regressor` do Prophet não modela estruturas de defasagem, pois as variáveis exógenas são fornecidas como valores contemporâneos
- Os modelos são retreinados do zero a cada execução, sem persistência de modelo implementada

**XGBoost com variáveis exógenas — viés de reversão à média**  
Esta é a limitação mais significativa identificada no projeto. Apesar do ajuste adequado de hiperparâmetros, o XGBoost com variáveis exógenas converge para uma previsão quase constante próxima à média histórica do IPCA (~0,49%), independentemente dos valores reais de entrada para um determinado mês.

A causa raiz é arquitetural. O XGBoost utiliza divisões em árvore para particionar o espaço de features em regiões, e como as variáveis macroeconômicas (SELIC, câmbio e IGP-M) permanecem dentro de faixas historicamente estáveis ao longo do período de treinamento, o modelo aprende que "quando as condições macro são assim, o IPCA tende a ficar em torno de 0,49%." O sinal do `ipca_lag1`, que impulsiona a variação significativa no Nível 3, é diluído pelo peso combinado das features macro apontando para a mesma região histórica.

Isso contrasta com o comportamento do Prophet, onde cada variável exógena atua como um componente linear independente, tornando o modelo diretamente sensível a mudanças de valor absoluto mesmo dentro de faixas estáveis. As mesmas variáveis macro que causam reversão à média no XGBoost chegam a melhorar as previsões do Prophet nos meses mais recentes.

Essa descoberta ilustra um princípio mais amplo: pontuações de importância de features não garantem poder preditivo. Uma variável pode ter alta importância no modelo sem que isso resulte em variação significativa nas previsões.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
