import streamlit as st
from utils.data_loaders import load_experience_data
from utils.plots import plot_experience_distribution

def experience_analysis():
    st.title("Experience Analysis")
    st.markdown("### Insights into user experience clusters.")

    # Load experience data
    df_experience = load_experience_data()

    # Visualize experience scores
    st.markdown("#### Experience Score Distribution")
    fig = plot_experience_distribution(df_experience)
    st.plotly_chart(fig)

if __name__ == "__main__":
    experience_analysis()
