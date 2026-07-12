[🇧🇷 Versão em Português](README.pt.md)

# 📈 IPCA Forecasting — Prophet vs XGBoost

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Prophet](https://img.shields.io/badge/Prophet-0066CC?style=for-the-badge&logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-EA4335?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

Forecasting Brazil's official monthly inflation index (IPCA) using Prophet and XGBoost, with and without macroeconomic exogenous variables, structured across 4 progressive levels of complexity.

---

## 📋 Description

This project builds a complete time series forecasting pipeline for the IPCA (Broad Consumer Price Index), Brazil's official inflation index calculated by IBGE. The project compares two fundamentally different modeling approaches: a decomposition-based model (Prophet) and a gradient boosting model (XGBoost), across multiple levels of complexity, with and without macroeconomic variables.

All data is fetched live from the Brazilian Central Bank's SGS API, keeping every notebook self-contained, reproducible, and always up to date with the latest available month.

---

## 🗂️ Project Structure

The project is divided into 3 notebooks, each self-contained and reproducible:

| Notebook | Content |
|---|---|
| `01_EDA_e_Extracao.ipynb` | Exploratory Data Analysis: data ingestion, distribution analysis, stationarity tests (ADF/KPSS), ACF/PACF |
| `02_Modelagem_Prophet.ipynb` | Levels 1 and 2: Prophet without and with exogenous variables |
| `03_XGBoost_Modelagem.ipynb` | Levels 3 and 4: XGBoost without and with exogenous variables |

### Level Progression

| Level | Model | Features | Highlights |
|---|---|---|---|
| 1 | Prophet (pure) | IPCA historical series | Stable baseline that captures long-term trend and annual seasonality |
| 2 | Prophet + Regressors | IPCA + SELIC, exchange rate, IGP-M | Sensitive to macro shifts with stronger alignment to recent inflation trajectory |
| 3 | XGBoost (pure) | IPCA lags + calendar features | Best aggregate MAE driven by strong AR(1) autocorrelation structure |
| 4 | XGBoost + Exogenous | IPCA lags + lagged macro variables | Mean reversion bias where macro variables dilute the lag signal |

---

## 📦 Data Sources

All data is fetched directly from the **Brazilian Central Bank SGS API** at runtime, with no static files required.

| Variable | Description | SGS Code |
|---|---|---|
| IPCA | Brazil's official monthly inflation index (IBGE) | 433 |
| SELIC | Brazil's benchmark interest rate (COPOM) | 4189 |
| Exchange Rate | USD/BRL monthly rate | 3698 |
| IGP-M | General Market Price Index (wholesale inflation proxy) | 189 |

**Training period:** January 2000 to December 2025  
**Holdout period:** January 2026 onwards, updated automatically as new months are released

---

## 🛠️ Built With

- Python
- Pandas / NumPy
- Prophet (Meta)
- XGBoost
- Scikit-Learn (`RandomizedSearchCV`, `TimeSeriesSplit`)
- Matplotlib
- Statsmodels
- Requests (BCB SGS API)

---

## ⚙️ How to Run

### Prerequisites

```bash
pip install pandas numpy matplotlib requests statsmodels prophet xgboost scikit-learn
```

### Steps

1. Clone the repository
```bash
git clone https://github.com/Marques07/IPCA-Prophet-vs-XGBoost.git
```

2. Open the notebooks in order:
   - Start with `01_EDA_e_Extracao.ipynb` for context
   - Run `02_Modelagem_Prophet.ipynb` for Prophet models (recommended: Google Colab)
   - Run `03_XGBoost_Modelagem.ipynb` for XGBoost models (VS Code or Jupyter)

> **Note:** Prophet installation can be tricky on Windows. Google Colab is recommended for the Prophet notebook.

---

## 📊 Results & Model Selection

Aggregate MAE across the full 2026 holdout favors XGBoost (pure), driven by the strong AR(1) structure of the IPCA series. However, aggregate metrics alone do not tell the full story.

Prophet with exogenous variables has demonstrated increasing accuracy as more 2026 months become available, capturing the inflation trajectory more closely in recent months. For the purpose of next-month forecasting, where recent trend alignment matters more than historical average error, Prophet with regressors has shown stronger real-world predictive behavior.

XGBoost (pure) remains the most consistent model on aggregate, but its forecasts show less sensitivity to current macroeconomic conditions. XGBoost with exogenous variables exhibits mean reversion bias, converging toward the historical mean regardless of input variation.

> Metrics are recalculated automatically on each run as new months become available. Refer to the notebook outputs for current MAE and RMSE values.

---

## 🔍 Key Findings

**Prophet (pure) vs Prophet + Exogenous**  
Adding SELIC, exchange rate, and IGP-M as regressors to Prophet increased average error on early holdout months. Prophet's `add_regressor` assumes an instantaneous linear relationship between the regressor and the target, but in practice SELIC affects inflation with a 6 to 12 month lag. However, as 2026 progressed, the model with regressors demonstrated stronger alignment with the real inflation curve, suggesting it learns the macroeconomic context more effectively over time.

**XGBoost (pure) — best aggregate result**  
XGBoost achieved the lowest aggregate MAE, with `ipca_lag1` as the dominant feature, confirming the strong AR(1) structure identified in the ACF/PACF analysis. The model captures short-term momentum well but struggles with abrupt spikes that have no precedent in the immediate past lags.

**XGBoost + Exogenous — mean reversion bias**  
Despite IGP-M lag 1 and lag 2 ranking as the 2nd and 3rd most important features, the model converges toward the historical mean, producing near-constant predictions regardless of input variation. This occurs because the macro variables remain within historically stable ranges, diluting the `ipca_lag1` signal that drives variation in Level 3. This illustrates that feature importance scores alone do not guarantee predictive power.

**Prophet vs XGBoost — architectural difference**  
Prophet treats each exogenous variable as an independent linear component, making it directly sensitive to absolute value changes. XGBoost treats all features equally in tree splits, requiring macro variables to fall outside historical norms to produce meaningfully different predictions. This fundamental difference explains why Prophet with regressors adapts better to recent macroeconomic shifts, while XGBoost pure excels at capturing stable autocorrelation patterns.

---

## 🔮 Live Forecast

Both notebooks include a **Live Forecast** section that automatically generates a prediction for the next unreleased IPCA month. Once IBGE publishes the official figure, the prediction can be compared against the result to validate the models in a real-world scenario.

---

## ⚠️ Limitations


- Holdout window grows automatically as new months are released, so metrics improve over time
- Prophet's `add_regressor` does not model lag structures, as exogenous variables are fed as contemporaneous values
- Models are retrained from scratch on each run, with no model persistence implemented

**XGBoost with exogenous variables — mean reversion bias**  
This is the most significant limitation identified in the project. Despite proper hyperparameter tuning, XGBoost with exogenous variables converges toward a near-constant prediction close to the historical IPCA mean (~0.49%), regardless of what the actual input values are for a given month.

The root cause is architectural. XGBoost uses tree splits to partition the feature space into regions, and since the macro variables (SELIC, exchange rate, and IGP-M) remain within historically stable ranges throughout the training period, the model learns that "when macro conditions look like this, IPCA tends to be around 0.49%." The `ipca_lag1` signal that drives meaningful variation in Level 3 gets diluted by the combined weight of the macro features pointing to the same historical region.

This contrasts with Prophet's behavior, where each exogenous variable acts as an independent linear component, making the model directly sensitive to absolute value changes even within stable ranges. The same macro variables that cause mean reversion in XGBoost actually improve Prophet's forecasts in recent months.

This finding illustrates a broader principle: feature importance scores do not guarantee predictive power. A variable can rank highly in importance while the model still fails to produce meaningful variation in its predictions.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
