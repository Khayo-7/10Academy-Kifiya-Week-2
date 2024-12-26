import plotly.express as px

def plot_user_distribution(df):
    return px.histogram(df, x="Cluster", color="Cluster", title="User Cluster Distribution")

def plot_engagement_distribution(df):
    return px.histogram(df, x="Engagement Score", color="Cluster", title="Engagement Scores by Cluster")

def plot_engagement_boxplot(df):
    return px.box(df, y="Engagement Score", color="Cluster", title="Engagement Score Spread")

def plot_experience_distribution(df):
    return px.box(df, y="Experience Score", color="Cluster", title="Experience Score Spread")

def plot_satisfaction_scores(df):
    top_users = df.sort_values("Satisfaction Score", ascending=False).head(10)
    return px.bar(top_users, x="User ID", y="Satisfaction Score", color="Satisfaction Score", title="Top 10 Satisfied Customers")

def plot_engagement_vs_experience(df):
    return px.scatter(
        df,
        x="Engagement Score",
        y="Experience Score",
        color="Cluster",
        title="Engagement vs Experience Score",
        size="Total Traffic",
        hover_name="User ID",
    )

def plot_user_cluster_pie(df):
    cluster_counts = df['Cluster'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster', 'Count']
    return px.pie(cluster_counts, values='Count', names='Cluster', title="Cluster Distribution (Pie Chart)")

def plot_user_traffic_vs_satisfaction(df):
    return px.scatter(
        df,
        x="Total Traffic",
        y="Satisfaction Score",
        color="Cluster",
        size="Engagement Score",
        title="Traffic vs Satisfaction by Cluster",
        hover_name="User ID",
    )

def plot_time_on_network_distribution(df):
    return px.box(df, x="Cluster", y="Time on Network", color="Cluster", title="Time on Network by Cluster")

def plot_combined_metrics(df):
    return px.parallel_coordinates(
        df,
        dimensions=["Engagement Score", "Experience Score", "Satisfaction Score"],
        color="Cluster",
        title="Parallel Coordinates of Metrics by Cluster",
    )
