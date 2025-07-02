# ⚡ Energy-Demand-Prediction

This project focuses on evaluating machine learning models to accurately forecast energy demand using historical energy consumption and weather data.

---

## 📌 Overview

The goal is to build and test predictive models that can anticipate energy demand based on historical patterns and meteorological conditions. The pipeline includes:

- Collecting and preprocessing time-series data
- Training machine learning models in Python
- Validating predictions using real-time data

---

## 📊 Data Sources

### 1. Historical Energy Data
- **Source**: [Open Power System Data – Time Series](https://data.open-power-system-data.org/time_series/)
- **File**: `time_series_60min_singleindex.csv`
- **Description**: Hourly time-series data including electricity consumption, generation, and market data for various European countries.
- **Documentation**: [Dataset Notebook](https://nbviewer.org/github/Open-Power-System-Data/datapackage_timeseries/blob/2020-10-06/main.ipynb)

### 2. Weather Data
- **Source**: [Open-Meteo API](https://open-meteo.com/)
- **Use**: Provides historical and forecast weather metrics such as temperature, wind speed, and cloud cover used to improve demand predictions.

### 3. Real-Time Validation Data
- **Source**: [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)
- **Use**: Used to validate the trained models against real-time electricity demand.

---

## 🛠️ Tools & Technologies

- **Python**  
- **Jupyter Notebooks**  
- **Pandas, NumPy, Scikit-learn, XGBoost**  
- **Matplotlib / Seaborn for Visualization**  
- **APIs** for fetching weather and real-time data

---

## 🚀 Workflow

1. **Data Collection** – Fetch historical energy and weather data.
2. **Preprocessing** – Clean, merge, and format datasets for model input.
3. **Model Training** – Train ML models such as Random Forest, XGBoost, or LSTM.
4. **Evaluation** – Assess model performance on validation sets.
5. **Real-Time Validation** – Test model performance using live ENTSO-E data.

---

## 📂 Project Structure

```plaintext
├── data/                   # Raw and processed data files
├── notebooks/              # Jupyter notebooks for exploration and modeling
├── models/                 # Saved models
├── scripts/                # Python scripts for data handling and model training
├── README.md
