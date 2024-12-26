import streamlit as st

def apply_custom_styling():
    st.markdown(
        """
        <style>
        .css-1q1biag {background: #f8f9fa;} /* Light sidebar background */
        .sidebar-content {padding: 30px;}
        h1, h2, h3, h4, h5 {font-family: 'Arial', sans-serif;}
        .block-container {padding: 20px 30px;}
        </style>
        """,
        unsafe_allow_html=True,
    )
