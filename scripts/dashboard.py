import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from preprocessing.data_loaders import load_data_using_sqlalchemy
from preprocessing.data_cleaning import clean_data
from preprocessing.data_transformation import transform_data
from vizualize import plot_data, plot_histogram, plot_boxplot, plot_scatter, plot_correlation_matrix

# Load the telecom data
@st.cache_data
def load_data():
    """Load dataset from the PostgreSQL database."""
    try:
        return load_data_using_sqlalchemy("SELECT * FROM xdr_data;")
    except Exception as e:
        st.error(f"Failed to load data from the PostgreSQL database: {e}")
        return pd.DataFrame()

# Data loading and preprocessing
df = load_data()
if not df.empty:
    df_cleaned = clean_data(df)
    # df_transformed = transform_data(df_cleaned)

    # Dashboard title and introduction
    st.title("Telecom Data Visualization and Exploration")
    st.write("""
    This interactive dashboard allows you to explore telecom data through various visualization techniques. 
    Use the tabs below to navigate through different types of plots.
    """)

    # Tabbed layout for visualizations
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        ["Scatter Plot", "Bar Chart", "Histogram", "Boxplot", "Pairplot", "Correlation Matrix", "Distribution Plot"]
    )

    # Scatter Plot Tab
    with tab1:
        st.subheader("Scatter Plot")
        x_axis = st.selectbox("Select X-axis variable:", df_cleaned.columns, key="scatter_x")
        y_axis = st.selectbox("Select Y-axis variable:", df_cleaned.columns, key="scatter_y")
        scatter_color = st.color_picker("Pick a color:", "#1f77b4")
        fig = plot_data(
            df_cleaned, plot_type='scatter', x=x_axis, y=y_axis, 
            title=f"Scatter Plot of {x_axis} vs {y_axis}", color=scatter_color
        )
        st.pyplot(fig)

    # Bar Chart Tab
    with tab2:
        st.subheader("Bar Chart")
        bar_column = st.selectbox("Select column for Bar Chart:", df_cleaned.columns, key="bar_column")
        fig = plot_data(df_cleaned, plot_type='bar', x=bar_column, title=f"Bar Chart of {bar_column}")
        st.pyplot(fig)

    # Histogram Tab
    with tab3:
        st.subheader("Histogram")
        hist_column = st.selectbox("Select column for Histogram:", df_cleaned.columns, key="hist_column")
        bins = st.slider("Select number of bins:", 5, 100, 20)
        kde_option = st.checkbox("Overlay KDE Curve", value=True)
        fig = plot_data(
            df_cleaned, plot_type='histogram', x=hist_column, bins=bins, kde=kde_option, 
            title=f"Histogram of {hist_column}"
        )
        st.pyplot(fig)

    # Boxplot Tab
    with tab4:
        st.subheader("Boxplot")
        box_column = st.selectbox("Select column for Boxplot:", df_cleaned.columns, key="box_column")
        fig = plot_data(
            df_cleaned, plot_type='boxplot', x=box_column, title=f"Boxplot of {box_column}"
        )
        st.pyplot(fig)

    # Pairplot Tab
    with tab5:
        st.subheader("Pairplot")
        selected_columns = st.multiselect(
            "Select columns for Pairplot (up to 5):", df_cleaned.columns, default=df_cleaned.columns[:5]
        )
        if len(selected_columns) > 1:
            fig = sns.pairplot(df_cleaned[selected_columns])
            st.pyplot(fig)

    # Correlation Matrix Tab
    with tab6:
        st.subheader("Correlation Matrix")
        fig = plot_correlation_matrix(
            df_cleaned, df_cleaned.select_dtypes(include='number').columns
        )
        st.pyplot(fig)

    # Distribution Plot Tab
    with tab7:
        st.subheader("Distribution Plot")
        dist_column = st.selectbox("Select column for Distribution Plot:", df_cleaned.columns, key="dist_column")
        shade_option = st.checkbox("Shade under the curve", value=True)
        fig = plot_data(
            df_cleaned, plot_type='kde', x=dist_column, shade=shade_option, 
            title=f"Distribution Plot of {dist_column}"
        )
        st.pyplot(fig)

else:
    st.error("No data available to display. Please check the database connection or query.")

