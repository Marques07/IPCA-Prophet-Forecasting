[🇧🇷 Versão em Português](README.pt.md)

# 📈 IPCA Forecasting with Prophet

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Prophet](https://img.shields.io/badge/Prophet-0066CC?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

Forecasting Brazil's official monthly inflation index (IPCA) using Prophet, with and without macroeconomic exogenous variables, structured across 2 progressive levels of complexity.

---

## 📋 Description

This project builds a complete time series forecasting pipeline for the IPCA (Broad Consumer Price Index), Brazil's official inflation index calculated by IBGE. The project compares two Prophet configurations: a pure seasonal model (Level 1) and a model enriched with macroeconomic exogenous variables (Level 2).

All data is fetched live from the Brazilian Central Bank's SGS API, keeping every notebook self-contained, reproducible, and always up to date with the latest available month.

---

## 🗂️ Project Structure

The project is divided into 2 notebooks, each self-contained and reproducible:

| Notebook | Content |
|---|---|
| `01_EDA_e_Extracao.ipynb` | Exploratory Data Analysis: data ingestion, distribution analysis, stationarity tests (ADF/KPSS), ACF/PACF |
| `02_Modelagem_Prophet.ipynb` | Prophet modeling: Level 1 (pure) and Level 2 (with exogenous variables), plus an appendix with technical diagnostics |

### Level Progression

| Level | Model | Features | Highlights |
|---|---|---|---|
| 1 | Prophet (pure) | IPCA historical series | Stable baseline that captures long-term trend and annual seasonality without external input |
| 2 | Prophet + Regressors | IPCA + SELIC, exchange rate, IGP-M | Sensitive to macro shifts; aligns more closely with the recent inflation trajectory |

---

## 📦 Data Sources

All data is fetched directly from the **Brazilian Central Bank SGS API** at runtime, with no static files required.

| Variable | Description | SGS Code |
|---|---|---|
| IPCA | Brazil's official monthly inflation index (IBGE) | 433 |
| SELIC | Brazil's benchmark interest rate (COPOM) | 4189 |
| Exchange Rate | USD/BRL monthly rate | 3698 |
| IGP-M | General Market Price Index (wholesale inflation proxy) | 189 |

**Training period:** January 2000 through the end of the previous year (filtered to exclude the pre-Plano Real hyperinflation regime)  
**Holdout period:** current year, updated automatically as new months are released

---

## 🛠️ Built With

- Python
- Pandas / NumPy
- Prophet (Meta)
- Scikit-Learn (evaluation metrics)
- Matplotlib
- Statsmodels (ADF, KPSS, ACF, PACF)
- Requests (BCB SGS API)

---

## ⚙️ How to Run

### Prerequisites

```bash
pip install pandas numpy matplotlib requests statsmodels prophet scikit-learn
```

### Steps

**Option A — Run in Google Colab (recommended):**

1. Click the badge below to open the main notebook directly in Colab:

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Marques07/IPCA-Prophet-Forecasting/blob/main/02_Modelagem_Prophet.ipynb)

2. In Colab, go to **Runtime → Run all** (or run cells manually)
3. All dependencies are pre-installed in Colab, except Prophet — the notebook handles the installation in the first cell

**Option B — Run locally:**

1. Clone the repository:
   ```bash
   git clone https://github.com/Marques07/IPCA-Prophet-Forecasting.git
   ```

2. Open the notebooks in order:
   - Start with `01_EDA_e_Extracao.ipynb` for context
   - Run `02_Modelagem_Prophet.ipynb` for the Prophet models

> **Note:** Prophet installation can be tricky on Windows. Google Colab is recommended.

---

## 📊 Results & Model Selection

Level 2 (Prophet + exogenous variables) clearly outperforms Level 1, both visually and in the holdout metrics. The forecast from Level 2 tracks the actual IPCA trajectory much more closely, especially during months where macroeconomic conditions shift abruptly.

The reason is straightforward: the exogenous variables give the model context that the seasonal pattern alone cannot provide. When SELIC, exchange rate, and IGP-M move, they carry information about where inflation is heading. Level 1 only sees the calendar; Level 2 sees the calendar *and* the macro environment.

A caveat: Prophet's `add_regressor` assumes exogenous variables affect inflation immediately, while in reality SELIC transmits with a 6-to-12-month lag. Even with this simplification, the added context makes a clear difference.

> **Important note on interpretation:** the Level 2 forecast uses the *actual* values of SELIC, exchange rate, and IGP-M during the test period — not predictions. This means Level 2 answers the question "given what we know about the macro environment, what should IPCA be?" rather than "what will IPCA be, without any future information?". This is a common and valid setup for conditional forecasting.

> **Key finding on retraining:** a walk-forward validation (available in the notebook's appendix) showed only modest improvement over the frozen model. This suggests that, for this dataset, adding exogenous information (Level 2) provides a larger predictive gain than periodically retraining on more historical data.

---

## 🔮 Live Forecast

Both notebooks include a **Live Forecast** section that automatically generates a prediction for the next unreleased IPCA month. Once IBGE publishes the official figure, the prediction can be compared against the result to validate the model in a real-world scenario.

---

## 🔬 Appendix — Technical Diagnostics

The Prophet notebook includes an appendix with supplementary diagnostics, kept separate from the main pipeline:

1. **Prophet Component Decomposition** — how the model splits the IPCA series into trend and yearly seasonality
2. **Time-Series Cross-Validation** — Prophet's built-in cross-validation across multiple historical windows (Level 1 and Level 2)
3. **Walk-Forward Validation** — comparison between a frozen model and a periodically retrained model, simulating a production pipeline

---

## ⚠️ Limitations

- **Holdout window is dynamic:** the test set is the current year-to-date, so it grows as new months are released. This mirrors real-world usage but means metrics evolve month to month rather than being directly comparable across runs.
- **Instantaneous regressor assumption:** `add_regressor` treats each exogenous variable as having a contemporaneous effect on IPCA. In practice, variables like SELIC transmit with a 6-to-12-month lag, so the model captures only part of the causal chain. This is a known simplification of Prophet rather than a bug.
- **No model persistence:** the model is retrained on each run. This keeps the notebook fully self-contained and reproducible, but would need to be adapted for a production deployment where model artifacts are versioned and cached.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
