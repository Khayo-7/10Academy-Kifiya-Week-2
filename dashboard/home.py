import streamlit as st
from utils.styles import apply_custom_styling

# Global configuration
st.set_page_config(
    page_title="Telecom Insights Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Telecom Dashboard for user engagement, experience, and satisfaction analysis."
    },
)

# Apply custom styling
apply_custom_styling()

# Main dashboard
def main():
    st.title("📊 Telecom Insights Dashboard")
    st.markdown(
        """
        Welcome to the **Telecom Insights Dashboard**!
        
        This dashboard provides an in-depth analysis of user behavior and satisfaction metrics across key areas such as:
        - **User Overview**: Demographics and high-level KPIs.
        - **Engagement Analysis**: Engagement score trends and patterns.
        - **Experience Analysis**: Customer experience ratings and insights.
        - **Satisfaction Analysis**: Insights into satisfaction levels.

        Use the **sidebar** to navigate to different sections of the dashboard and explore the analytics.
        """
    )

    # Sample Call-to-Action or Highlights
    st.markdown(
        """
        ### Highlights
        - 👥 Total Users Analyzed: **5,000+**
        - 🎯 Engagement Score Range: **1-100**
        - 📶 Clusters Identified: **8**
        - 🌟 Top Customer Satisfaction Score: **98/100**
        """
    )

    # # Add navigation buttons
    # st.markdown("#### Quick Navigation")
    # col1, col2, col3, col4 = st.columns(4)
    # if col1.button("User Overview"):
    #     st.query_params(page="user_overview")
    # if col2.button("Engagement Analysis"):
    #     st.query_params(page="engagement_analysis")
    # if col3.button("Experience Analysis"):
    #     st.query_params(page="experience_analysis")
    # if col4.button("Satisfaction Analysis"):
    #     st.query_params(page="satisfaction_analysis")

    # # Placeholder in case of page query params
    # current_page = st.query_params().get("page", ["home"])[0]
    # if current_page == "user_overview":
    #     from pages.A_User_Overview import show_overview
    #     show_overview()
    # elif current_page == "engagement_analysis":
    #     from pages.B_Satisfaction_Analysis import show_engagement
    #     show_engagement()
    # elif current_page == "experience_analysis":
    #     from pages.C_Experience_Analysis import show_experience
    #     show_experience()
    # elif current_page == "satisfaction_analysis":
    #     from pages.D_Engagement_Analysis import show_satisfaction
    #     show_satisfaction()

if __name__ == "__main__":
    main()


# st.sidebar.title("📊 Navigation")
# # Navigation and Sidebar
# def sidebar_navigation():
#     page = st.sidebar.radio(
#         "Navigate Pages",
#         ["Users Overview", "Engagement Analysis", "Experience Analysis", "Satisfaction Analysis"],
#     )
#     # st.sidebar.markdown("📂 Explore user behavior and KPIs.")
#     return page

# page = sidebar_navigation()

# # Route to selected page
# if page == "Users Overview":
#     from pages.User_Overview import show_overview
#     show_overview()
# elif page == "Engagement Analysis":
#     from pages.Engagement_Analysis import show_engagement
#     show_engagement()
# elif page == "Experience Analysis":
#     from pages.Experience_Analysis import show_experience
#     show_experience()
# elif page == "Satisfaction Analysis":
#     from pages.Satisfaction_Analysis import show_satisfaction
#     show_satisfaction()
