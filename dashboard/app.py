import streamlit as st

# Set up general configurations
st.set_page_config(
    page_title="Customer Insights Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("📊 Navigation")
st.sidebar.markdown("Navigate through the analysis sections:")

# Provide an overview
st.title("📈 Customer Insights Dashboard")
st.markdown("""
This dashboard provides an in-depth analysis of customer engagement, experience, and satisfaction. 
Use the sidebar to navigate through different analytical sections.
""")

# Add a custom sidebar logo or style
st.markdown(
    """
    <style>
    .css-1q1biag {background: #f8f9fa;} /* Adjust background */
    .sidebar .sidebar-content {padding: 30px;}
    </style>
    """,
    unsafe_allow_html=True,
)
# Sidebar KPI Summary
with st.sidebar:
    st.metric("Total Users", "89,700")
    st.metric("Clusters Identified", "4")
    st.metric("Average Satisfaction", "78.2%")

