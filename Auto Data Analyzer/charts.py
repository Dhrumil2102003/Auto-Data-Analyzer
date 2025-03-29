import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Bar Chart
def bar_chart(df, x_col, y_col):
    fig = px.bar(df, x=x_col, y=y_col, text_auto=True, color=x_col, template="plotly_dark")
    return fig

# Pie Chart
def pie_chart(df, column):
    pie_data = df[column].value_counts().reset_index()
    pie_data.columns = [column, "Count"]
    fig = px.pie(pie_data, names=column, values="Count", hole=0.3, template="seaborn")
    return fig

# Scatter Plot
def scatter_plot(df, x_col, y_col):
    fig = px.scatter(df, x=x_col, y=y_col, color=x_col, template="plotly_dark")
    return fig

# Time Series Chart
def time_series(df, date_col, value_col):
    fig = px.line(df, x=date_col, y=value_col, template="plotly_dark", markers=True)
    return fig

# Correlation Heatmap
def heatmap_corr(df):
    num_cols = df.select_dtypes(include=['number']).columns
    corr_matrix = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    return fig

# Data Table Display
def show_table(df):
    st.dataframe(df)
