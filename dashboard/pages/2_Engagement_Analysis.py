import streamlit as st
from utils.data_loaders import load_engagement_data
from utils.plots import plot_engagement_distribution, plot_engagement_boxplot, plot_engagement_vs_experience, plot_combined_metrics

def show_engagement():
    st.title("📊 User Engagement Analysis")
    st.markdown("### Explore User Engagement Patterns.")
    
    df_engagement = load_engagement_data()

    # KPIs
    col1, col2 = st.columns(2)
    col1.metric("Max Engagement Score", df_engagement["Engagement Score"].max())
    col2.metric("Min Engagement Score", df_engagement["Engagement Score"].min())

    # Visualize engagement distribution
    st.markdown("#### Engagement Distribution by Cluster")
    fig_dist = plot_engagement_distribution(df_engagement)
    st.plotly_chart(fig_dist)

    st.markdown("#### Engagement Score Spread")
    fig_box = plot_engagement_boxplot(df_engagement)
    st.plotly_chart(fig_box)

    st.markdown("#### Engagement vs Experience")
    fig_comparison = plot_engagement_vs_experience(df_engagement)
    st.plotly_chart(fig_comparison)

    # Combined Metrics
    st.markdown("#### Multivariate Insights Across Metrics")
    fig_combined_metrics = plot_combined_metrics(df_engagement)
    st.plotly_chart(fig_combined_metrics)
    
if __name__ == "__main__":
    show_engagement()
