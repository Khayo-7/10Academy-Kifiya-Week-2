import plotly.express as px

def plot_user_distribution(df):
    return px.histogram(df, x="Cluster", color="Cluster", title="User Cluster Distribution")

def plot_engagement_scores(df):
    return px.box(df, y="Engagement Score", color="Cluster", title="Engagement Scores per Cluster")

def plot_experience_distribution(df):
    return px.box(df, y="Experience Score", color="Cluster", title="Experience Scores Distribution")

def plot_satisfaction_scores(df):
    return px.bar(
        df.sort_values("Satisfaction Score", ascending=False).head(10),
        x="User ID",
        y="Satisfaction Score",
        color="Satisfaction Score",
        title="Top 10 Satisfied Customers",
    )

# Cluster distribution
def plot_user_overview(df):
    return px.histogram(df, x="Cluster", color="Cluster", title="User Cluster Distribution")

# Engagement by cluster
def plot_engagement_distribution(df):
    return px.histogram(df, x="Engagement Score", color="Cluster", title="Engagement Scores by Cluster")

# Engagement spread
def plot_engagement_boxplot(df):
    return px.box(df, y="Engagement Score", color="Cluster", title="Engagement Score Spread")
