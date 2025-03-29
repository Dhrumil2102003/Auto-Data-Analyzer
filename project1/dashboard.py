import streamlit as st
import plotly.express as px

def show_dashboard(df):
    st.subheader("Customizable Data Dashboard")

    # Allow user to select columns to include
    selected_columns = st.sidebar.multiselect("Select Columns to Display", df.columns.tolist(), default=df.columns.tolist())
    df = df[selected_columns]  # Update dataframe based on selection

    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    st.sidebar.subheader("\U0001F6E0 Customize Dashboard")
    selected_charts = st.sidebar.multiselect("Choose Charts to Display", ["KPIs", "Bar Chart", "Pie Chart", "Time Series"])

    if "KPIs" in selected_charts and num_cols:
        st.subheader("\U0001F4CA Key Performance Indicators (KPIs)")
        cols = st.columns(min(3, len(num_cols)))
        for i, col in enumerate(num_cols[:3]):
            cols[i].metric(col, f"{df[col].sum():,.2f}")

    if "Bar Chart" in selected_charts and cat_cols and num_cols:
        selected_cat = st.sidebar.selectbox("Select Categorical Column", cat_cols)
        selected_num = st.sidebar.selectbox("Select Numerical Column", num_cols)
        
        st.subheader(f"\U0001F4CA {selected_cat} vs {selected_num}")
        bar_data = df.groupby(selected_cat)[selected_num].sum().reset_index()
        fig = px.bar(bar_data, x=selected_cat, y=selected_num, color=selected_cat, text_auto=True, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    if "Pie Chart" in selected_charts and cat_cols:
        selected_pie_cat = st.sidebar.selectbox("Select Column for Pie Chart", cat_cols)
        
        st.subheader(f"\U0001F967 Distribution of {selected_pie_cat}")
        pie_data = df[selected_pie_cat].value_counts().reset_index()
        pie_data.columns = [selected_pie_cat, "Count"]
        fig = px.pie(pie_data, names=selected_pie_cat, values="Count", hole=0.4, template="seaborn")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("\U0001F4CB View Data Sample"):
        st.write(df.head(50))
