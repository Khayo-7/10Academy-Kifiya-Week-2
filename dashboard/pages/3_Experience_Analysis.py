import streamlit as st
from utils.data_loaders import load_experience_data
from utils.plots import plot_experience_distribution, plot_time_on_network_distribution

def show_experience():
    st.title("🌟 Experience Analysis")
    st.markdown("Discover how users rate their experience.")

    # Load Data
    df_experience = load_experience_data()

    # Display Data
    st.markdown("#### Experience Data Overview")
    st.dataframe(df_experience.head(), height=300)

    # Plot
    st.markdown("#### Experience Score Distribution")
    fig = plot_experience_distribution(df_experience)
    st.plotly_chart(fig)

    # Time on Network Distribution
    st.markdown("#### Time on Network by Cluster")
    fig_time_on_network = plot_time_on_network_distribution(df_experience)
    st.plotly_chart(fig_time_on_network)

if __name__ == "__main__":
    show_experience()
