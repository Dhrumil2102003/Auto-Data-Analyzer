
# 📊 Smart Data Analyzer

A powerful, interactive Streamlit application for **automated data analysis**, **visualization**, and **machine learning modeling**. Just upload your dataset and start exploring — no coding required!

## 🚀 Features

### 📂 Upload and Clean Any Dataset
- Supports `.csv`, `.xlsx`, `.xls`, `.txt`
- Automatically cleans NaNs, duplicates, and renames columns
- Optional normalization: Min-Max, Z-score, Max-Abs, Robust

### 📊 Charts / EDA
- **Bar, Pie, Scatter, Line, Heatmap, Time Series**
- Filter columns before charting
- Use AI (Gemini API) to generate natural language **chart insights**
- Download charts as PNG

### 📈 Dashboard View
- Select and display KPIs
- Choose which charts to show (bar, pie, line)
- Download full dashboard as image

### 🤖 Machine Learning
- **Classification**: Decision Tree, KNN, SVM
- **Regression**: Linear Regression, Decision Tree, SVR
- **Clustering**: KMeans, Agglomerative, DBSCAN
- Encoding options: Label or One-Hot
- Train/Test split and performance metrics
- Predict on custom input values

---

## 📂 Folder Structure

```
├── app.py               # Main Streamlit app
├── charts.py            # Chart rendering functions using Plotly & Matplotlib
├── dashboard.py         # Dashboard layout and KPI generation
├── gamma3.py            # Uses Google Gemini API to explain charts
├── ml_models.py         # Machine Learning model runner
├── preprocess.py        # Data cleaning, outlier removal, normalization
├── utils.py             # Helpers to load, clean, save, detect date column
└── uploaded_datasets/   # Folder where uploaded datasets are saved
```

---

## 🧠 How to Run the App

### 🔧 Requirements

```bash
pip install streamlit pandas plotly seaborn scikit-learn matplotlib google-generativeai
```

### ▶️ Launch

```bash
streamlit run app.py
```

---

## 🔐 Note on Gemini API

- This app uses `Google Gemini API` to explain charts via `gamma3.py`.
- Update your `GEMINI_API_KEY` in `gamma3.py`:

```python
genai.configure(api_key="YOUR_KEY_HERE")
```
