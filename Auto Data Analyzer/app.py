import streamlit as st
import plotly.express as px
from utils import load_data, check_and_clean_data, get_date_column, save_dataset_to_database
from charts import bar_chart, pie_chart, scatter_plot, time_series, heatmap_corr, show_table
from preprocess import auto_rename_columns, remove_outliers
from io import BytesIO

# -------- Convert date columns --------
def convert_date_columns(df):
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col], errors='ignore')
        except:
            pass
    return df

# -------- Download Plotly chart --------
def download_chart(fig, filename="chart.png"):
    buf = BytesIO()
    try:
        fig.write_image(buf, format="png")
        st.download_button(label="📥 Download Chart as PNG", data=buf.getvalue(), file_name=filename, mime="image/png")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# ----------- Main App -----------
st.set_page_config(page_title="📊 Auto Data Analyzer", layout='wide')
st.title("📊 Smart Auto Data Analyzer with AI")

# -------- App Mode --------
st.sidebar.title("📂 App Mode")
app_mode = st.sidebar.radio("Choose Mode", ["Dashboard", "Charts/EDA"])

uploaded_file = st.sidebar.file_uploader("Upload Dataset", type=["csv", "xlsx", "xls", "txt"])

if uploaded_file:
    file_path = save_dataset_to_database(uploaded_file)
    st.sidebar.success(f"✅ Dataset saved to {file_path}")

    df = load_data(uploaded_file)
    df = check_and_clean_data(df)
    df = auto_rename_columns(df)
    df = convert_date_columns(df)

    if app_mode == "Dashboard":
        from dashboard import show_dashboard
        show_dashboard(df)

    elif app_mode == "Charts/EDA":
        # -------- Filters --------
        st.sidebar.subheader("🔎 Optional Filters")
        filter_cols = [col for col in df.columns if df[col].nunique() < 20]
        selected_filter_cols = st.sidebar.multiselect("Select Columns to Filter", filter_cols)

        selected_filters = {}
        for col in selected_filter_cols:
            unique_values = df[col].dropna().unique()
            selected_values = st.sidebar.multiselect(f"Filter '{col}' by:", options=unique_values)
            if selected_values:
                selected_filters[col] = selected_values

        for col, values in selected_filters.items():
            df = df[df[col].isin(values)]

        # -------- Data Preview --------
        st.subheader("📑 Cleaned Data Preview")
        show_table(df)

        # -------- Chart Selection --------
        chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart", "Scatter Plot", "Time Series", "Correlation Heatmap"])

        try:
            if chart_type == "Correlation Heatmap":
                fig = heatmap_corr(df)
                st.pyplot(fig)
                download_chart(fig, "Correlation_Heatmap.png")

            elif chart_type == "Bar Chart":
                col_x = st.sidebar.selectbox("Select X-axis", df.columns)
                col_y = st.sidebar.selectbox("Select Y-axis", df.columns)
                fig = bar_chart(df, col_x, col_y)
                st.plotly_chart(fig, use_container_width=True)
                download_chart(fig, "Bar_Chart.png")

            elif chart_type == "Pie Chart":
                col_name = st.sidebar.selectbox("Select Column for Pie Chart", df.columns)
                fig = pie_chart(df, col_name)
                st.plotly_chart(fig, use_container_width=True)
                download_chart(fig, "Pie_Chart.png")

            elif chart_type == "Scatter Plot":
                col_x = st.sidebar.selectbox("Select X-axis", df.columns)
                col_y = st.sidebar.selectbox("Select Y-axis", df.columns)
                fig = scatter_plot(df, col_x, col_y)
                st.plotly_chart(fig, use_container_width=True)
                download_chart(fig, "Scatter_Plot.png")

            elif chart_type == "Time Series":
                date_col = get_date_column(df)
                if date_col:
                    value_col = st.sidebar.selectbox("Value Column", df.columns)
                    fig = time_series(df, date_col, value_col)
                    st.plotly_chart(fig, use_container_width=True)
                    download_chart(fig, "Time_Series.png")
                else:
                    st.warning("⚠️ No Date column found for Time Series.")
        except Exception as e:
            st.error(f"⚠️ Chart error: {str(e)}")

else:
    st.info("👈 Upload a dataset to start analysis.")
