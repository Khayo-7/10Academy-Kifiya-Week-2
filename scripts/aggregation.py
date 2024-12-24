from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def aggregate_engagement_metrics(df):
    """
    Aggregates engagement metrics (session frequency, session duration, total traffic) per user (MSISDN).
    
    Args:
    - df (DataFrame): The dataframe containing session data with relevant columns such as 
                      ['MSISDN/Number', 'Dur. (ms)', 'Total UL (Bytes)', 'Total DL (Bytes)'].
    
    Returns:
    - DataFrame: A DataFrame containing aggregated metrics per user (MSISDN).
    """
    
    # Aggregate session frequency: Count the number of sessions per user (MSISDN)
    session_frequency = df.groupby('MSISDN/Number')['Dur. (ms)'].count().reset_index(name='Session Frequency')
    
    # Aggregate session duration: Sum the session duration for each user (MSISDN)
    session_duration = df.groupby('MSISDN/Number')['Dur. (ms)'].sum().reset_index(name='Total Session Duration')
    
    # Aggregate total traffic: Sum up both download and upload data for each user (MSISDN)
    total_traffic = df.groupby('MSISDN/Number')[['Total DL (Bytes)', 'Total UL (Bytes)']].sum().reset_index()
    total_traffic['Total Traffic'] = total_traffic['Total DL (Bytes)'] + total_traffic['Total UL (Bytes)']
    
    # Merge all aggregated metrics
    engagement_metrics = session_frequency.merge(session_duration, on='MSISDN/Number', how='inner') \
                                         .merge(total_traffic, on='MSISDN/Number', how='inner') 
    
    return engagement_metrics

def top_10_engagement(df_engagement):
    """
    Reports the top 10 users based on session frequency, session duration, and total traffic.
    
    Args:
    - df_engagement (DataFrame): The dataframe with aggregated engagement metrics.
    
    Returns:
    - Tuple: Three dataframes - Top 10 users by session frequency, session duration, and total traffic.
    """
    # Get top 10 customers by each engagement metric
    top_10_session_frequency = df_engagement.nlargest(10, 'Session Frequency')
    top_10_session_duration = df_engagement.nlargest(10, 'Total Session Duration')
    top_10_traffic = df_engagement.nlargest(10, 'Total Traffic')
    
    return top_10_session_frequency, top_10_session_duration, top_10_traffic
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def normalize_metrics(df_engagement, normalize_type='minmax'):
    """
    Normalizes the engagement metrics (SessionFrequency, TotalSessionDuration, TotalTraffic).
    
    Args:
    - df_engagement (DataFrame): DataFrame containing the engagement metrics (SessionFrequency, TotalSessionDuration, TotalTraffic).
    - normalize_type (str): Type of normalization - 'minmax' for Min-Max scaling or 'zscore' for Z-score normalization.
    
    Returns:
    - DataFrame: DataFrame with normalized metrics.
    """
    
    metrics = ['Session Frequency', 'Total Session Duration', 'Total Traffic']
    
    # Choose the scaler type based on the normalization requested
    if normalize_type == 'minmax':
        scaler = MinMaxScaler()
    elif normalize_type == 'zscore':
        scaler = StandardScaler()
    else:
        raise ValueError("Invalid normalize_type. Use 'minmax' or 'zscore'.")
    
    # Apply the normalization and return the updated DataFrame
    df_engagement[metrics] = scaler.fit_transform(df_engagement[metrics])
    
    return df_engagement


def kmeans_clustering(df_engagement, n_clusters=3):
    """
    Perform K-means clustering on the normalized engagement metrics.
    
    Args:
    - df_engagement (DataFrame): DataFrame with normalized engagement metrics (SessionFrequency, TotalSessionDuration, TotalTraffic).
    - n_clusters (int): Number of clusters for K-Means algorithm.
    
    Returns:
    - DataFrame: DataFrame with the cluster labels added for each user.
    """
    
    # Select the relevant metrics for clustering
    engagement_metrics = ['Session Frequency', 'Total Session Duration', 'Total Traffic']
    
    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_engagement['Cluster'] = kmeans.fit_predict(df_engagement[engagement_metrics])
    
    return df_engagement


def cluster_statistics(df_engagement):
    """
    Compute min, max, average, and total metrics for each engagement cluster.
    
    Args:
    - df_engagement (DataFrame): The DataFrame containing engagement metrics and cluster assignments.
    
    Returns:
    - DataFrame: A DataFrame containing cluster statistics.
    """
    return df_engagement.groupby('Cluster').agg(
        Min_Session_Frequency=('Session Frequency', 'min'),
        Max_Session_Frequency=('Session Frequency', 'max'),
        Avg_Session_Frequency=('Session Frequency', 'mean'),
        Total_Session_Frequency=('Session Frequency', 'sum'),
        Min_Total_Session_Duration=('Total Session Duration', 'min'),
        Max_Total_Session_Duration=('Total Session Duration', 'max'),
        Avg_Total_Session_Duration=('Total Session Duration', 'mean'),
        Total_Total_Session_Duration=('Total Session Duration', 'sum'),
        Min_Total_Traffic=('Total Traffic', 'min'),
        Max_Total_Traffic=('Total Traffic', 'max'),
        Avg_Total_Traffic=('Total Traffic', 'mean'),
        Total_Total_Traffic=('Total Traffic', 'sum'),
    ).reset_index()
    
def aggregate_application_traffic(df):
    """
    This function aggregates the application traffic for each user.
    
    Parameters:
    df (DataFrame): The DataFrame containing the application traffic data.
    
    Returns:
    DataFrame: The aggregated application traffic data.
    """
    
    application_columns = [
        'Social Media DL (Bytes)', 'Google DL (Bytes)', 'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)'
    ]
    
    agg_app_traffic = df[application_columns].fillna(0).sum().sort_values(ascending=False).reset_index()
    agg_app_traffic.columns = ['Application', 'Total Traffic (Bytes)']

    
    return agg_app_traffic

def agg_top_user_per_app(df):
    """
    Aggregates the total traffic per application and derives the top 10 most engaged users.
    
    Args:
    - df (DataFrame): DataFrame containing session data with application traffic columns (e.g., 'Social Media DL (Bytes)', 'Google DL (Bytes)').
    
    Returns:
    - DataFrame: Aggregated traffic for each user per application, and top 10 most engaged users per application.
    """
    
    application_columns = [
        'Social Media DL (Bytes)', 'Google DL (Bytes)', 'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)'
    ]
    
    # Calculate total traffic per application for each user
    for app_col in application_columns:
        df[f'{app_col}_TotalTraffic'] = df[app_col].fillna(0)
    
    # Aggregate total traffic per application
    app_traffic_aggregate = df.groupby('MSISDN/Number')[application_columns].sum().reset_index()
    
    # Derive the top 10 most engaged users per application
    top_users_per_app = app_traffic_aggregate[application_columns].apply(lambda x: x.sort_values(ascending=False).head(10))
    
    return top_users_per_app, app_traffic_aggregate
