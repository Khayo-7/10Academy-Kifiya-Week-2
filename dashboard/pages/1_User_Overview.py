import streamlit as st
from utils.data_loaders import load_user_data
from utils.plots import plot_user_overview

def user_overview():
    st.title("📊 User Overview")
    st.markdown("### High-Level Insights into Customer Demographics and Data.")
    
    # Load user data
    df_users = load_user_data()
    st.markdown("#### Overview of the Dataset")
    st.dataframe(df_users.head(), height=400)

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", df_users["User ID"].nunique())
    col2.metric("Average Traffic (Bytes)", f"{df_users['Total Traffic'].mean():,.2f}")
    col3.metric("Unique Clusters", df_users["Cluster"].nunique())

    # Plot: Distribution of Users per Cluster
    st.markdown("#### Cluster Distribution")
    fig = plot_user_overview(df_users)
    st.plotly_chart(fig)

if __name__ == "__main__":
    user_overview()
