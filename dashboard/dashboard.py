import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px


from scripts.vizualize import *
from scripts.aggregation import *
from scripts.preprocessing.data_cleaning import *
from scripts.preprocessing.data_loaders import *
from scripts.preprocessing.data_transformation import *

# Load the telecom data
@st.cache_data
def load_data():
    """Load dataset from the PostgreSQL database."""
    try:
        return load_data_using_sqlalchemy("SELECT * FROM xdr_data;")
    except Exception as e:
        st.error(f"Failed to load data from the PostgreSQL database: {e}")
        return pd.DataFrame()

        
# Load the data

# Load data (upload a file using Streamlit file uploader)
# uploaded_file = st.file_uploader("Choose a file", type="csv")
# st.sidebar.subheader("Upload your data")
# uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
# if uploaded_file:
#     df = load_data(uploaded_file)  # Load data directly from the uploaded file
#     df = pd.read_csv(uploaded_file)
#     st.write(df.head())  # Show first few rows of the uploaded file

# Load the data
df = load_data()
if not df.empty:
    df_cleaned = clean_dataframe(df)
    # df_transformed = transform_data(df_cleaned)

    # Aggregate engagement metrics and get top 10 users for each metric
    df_engagement = aggregate_engagement_metrics(df_cleaned)
    top_10_session_frequency, top_10_session_duration, top_10_traffic = top_10_engagement(df_engagement)
    df_normalized = normalize_features(df_engagement, normalize_type='minmax')    
    df_clustered = kmeans_clustering(df_normalized, n_clusters=3)    
    cluster_stats = cluster_statistics(df_clustered)    
    top_users_per_app = aggregate_application_traffic(df_cleaned)  

    # Dashboard title and introduction
    st.title("Telecom Data Visualization and Exploration")
    st.write("""
    This interactive dashboard allows you to explore telecom data through various visualization techniques. 
    Use the tabs below to navigate through different types of plots.
    """)

    # Tabbed layout for visualizations
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        ["Scatter Plot", "Bar Chart", "Histogram", "Boxplot", "Pairplot", "Correlation Matrix", "Distribution Plot", "User Engagement"]
    )

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Home", "Engagement Analysis", "Experience Analysis", "Satisfaction Analysis"]
    )
    
    if page == "Home":
        st.title("Telecom Analytics Dashboard")
        st.write("Welcome to the dashboard for user experience and satisfaction analysis.")

    elif page == "Engagement Analysis":
        st.title("Engagement Analysis")
        # Load saved engagement data
        engagement_data = pd.read_csv("user_scores.csv")
        fig = px.histogram(engagement_data, x="Engagement_Score", title="Engagement Scores Distribution")
        st.plotly_chart(fig)
    
    elif page == "Experience Analysis":
        st.title("Experience Analysis")
        # Load saved experience data
        experience_data = pd.read_csv("user_scores.csv")
        fig = px.histogram(experience_data, x="Experience_Score", title="Experience Scores Distribution")
        st.plotly_chart(fig)
    
    elif page == "Satisfaction Analysis":
        st.title("Satisfaction Analysis")
        # Load saved satisfaction data
        satisfaction_data = pd.read_csv("user_scores.csv")
        st.write("Top 10 Satisfied Users", satisfaction_data.nlargest(10, "Satisfaction_Score"))

if __name__ == "__main__":
    main()
