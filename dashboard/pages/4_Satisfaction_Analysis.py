import streamlit as st
from utils.data_loaders import load_combined_data
from utils.plots import plot_satisfaction_scores

def satisfaction_analysis():
    st.title("Satisfaction Analysis")
    st.markdown("### Overview of user satisfaction based on engagement and experience.")

    # Load data
    df_combined = load_combined_data()

    # Visualize satisfaction scores
    st.markdown("#### Top 10 Most Satisfied Customers")
    fig = plot_satisfaction_scores(df_combined)
    st.plotly_chart(fig)

    # KPIs
    st.markdown("#### Key Metrics")
    st.write(df_combined[["User ID", "Engagement Score", "Experience Score", "Satisfaction Score"]].head(10))

if __name__ == "__main__":
    satisfaction_analysis()
