import matplotlib.pyplot as plt
import seaborn as sns

def plot_data(dataframe, plot_type, x=None, y=None, **kwargs):
    """
    A general-purpose plotting function for Streamlit and Jupyter with explicit figure return.

    Args:
        dataframe (pd.DataFrame): The data to plot.
        plot_type (str): Type of plot ('histogram', 'boxplot', 'violinplot', 'scatter', 'heatmap', 'bar', 'kde').
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis (if applicable).
        **kwargs: Additional customization arguments.

    Returns:
        matplotlib.figure.Figure: The plot figure object.
    """
    # Explicitly create figure and axis
    fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
    
    if plot_type == 'histogram':
        sns.histplot(dataframe[x], 
                     bins=kwargs.get('bins', 10), 
                     kde=kwargs.get('kde', False), 
                     color=kwargs.get('color', 'skyblue'), 
                     edgecolor=kwargs.get('edgecolor', 'black'),
                     ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', 'Values'))
        ax.set_ylabel(kwargs.get('ylabel', 'Frequency'))

    elif plot_type == 'boxplot':
        sns.boxplot(x=dataframe[x], y=dataframe[y] if y else None, ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', y) if y else 'Values')

    elif plot_type == 'violinplot':
        sns.violinplot(x=dataframe[x] if x else None, y=dataframe[y] if y else None, ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', y) if y else 'Values')

    elif plot_type == 'scatter':
        ax.scatter(dataframe[x], dataframe[y], 
                   c=kwargs.get('color', 'blue'), 
                   alpha=kwargs.get('alpha', 0.5))
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', y))

    elif plot_type == 'heatmap':
        numeric_dataframe = dataframe.corr()  # Default is correlation heatmap
        sns.heatmap(numeric_dataframe, 
                    annot=kwargs.get('annot', True), 
                    cmap=kwargs.get('cmap', 'coolwarm'), 
                    fmt=kwargs.get('fmt', ".2f"), 
                    linewidths=kwargs.get('linewidths', 0.5),
                    ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', ''))
        ax.set_ylabel(kwargs.get('ylabel', ''))

    elif plot_type == 'bar':
        dataframe[x].value_counts().plot(kind='bar', 
                                         color=kwargs.get('color', 'lightgreen'), 
                                         edgecolor=kwargs.get('edgecolor', 'black'),
                                         ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', 'Frequency'))

    elif plot_type == 'kde':
        sns.kdeplot(dataframe[x], shade=kwargs.get('shade', True), ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', x))
    
    ax.set_title(kwargs.get('title', ''))
    plt.xticks(rotation=kwargs.get('xticks_rotation', 0))
    
    return fig
    # return plt.gcf()

def plot_histogram(df, columns, bins=15, title="Histograms", figsize=(12, 8)):
    """
    Plots histograms for the specified columns.
    
    Args:
        df (DataFrame): Dataset.
        columns (list): Columns to plot.
        bins (int): Number of bins for the histogram.
        title (str): Overall title for the histograms.
        figsize (tuple): Size of the figure.
    
    Returns:
        plt.Figure: Matplotlib figure object.
    """
    fig, axes = plt.subplots(1, len(columns), figsize=figsize)
    axes = axes if len(columns) > 1 else [axes]
    for col, ax in zip(columns, axes):
        df[col].plot(kind='hist', bins=bins, ax=ax, edgecolor='black')
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel(col)
    fig.suptitle(title)
    return fig

def plot_boxplot(df, columns, title="Boxplots", figsize=(12, 6)):
    """
    Plots boxplots for the specified columns.
    
    Args:
        df (DataFrame): Dataset.
        columns (list): Columns to plot.
        title (str): Overall title for the boxplots.
        figsize (tuple): Size of the figure.
    
    Returns:
        plt.Figure: Matplotlib figure object.
    """
    fig, axes = plt.subplots(1, len(columns), figsize=figsize)
    axes = axes if len(columns) > 1 else [axes]
    for col, ax in zip(columns, axes):
        sns.boxplot(y=df[col], ax=ax)
        ax.set_title(f'Boxplot for {col}')
    fig.suptitle(title)
    return fig

def plot_scatter(df, x, y, title="Scatter Plot", figsize=(8, 6)):
    """
    Plots a scatter plot for two variables.
    
    Args:
        df (DataFrame): Dataset.
        x (str): X-axis variable.
        y (str): Y-axis variable.
        title (str): Title of the scatter plot.
        figsize (tuple): Size of the figure.
    
    Returns:
        plt.Figure: Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=figsize)
    sns.scatterplot(data=df, x=x, y=y, ax=ax)
    ax.set_title(title)
    return fig

def plot_correlation_matrix(df, columns, title="Correlation Matrix", figsize=(8, 6)):
    """
    Plots a heatmap for the correlation matrix of specified columns.
    
    Args:
        df (DataFrame): Dataset.
        columns (list): Columns to include in the correlation matrix.
        title (str): Title of the heatmap.
        figsize (tuple): Size of the figure.
    
    Returns:
        plt.Figure: Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=figsize)
    correlation = df[columns].corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title(title)
    return fig

def plot_top_10(df_engagement, metric, xlabel, ylabel, title):
    """
    Plots the top 10 users based on the given metric and returns the figure.

    Args:
    - df_engagement (DataFrame): The dataframe containing engagement data.
    - metric (str): The column name to be used for the top 10 ranking (e.g., 'SessionFrequency', 'TotalSessionDuration', 'TotalTraffic').
    - xlabel (str): The label for the x-axis.
    - ylabel (str): The label for the y-axis.
    - title (str): The title of the plot.

    Returns:
    - fig: The matplotlib figure object.
    """
    top_10_df = df_engagement.nlargest(10, metric)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='MSISDN', y=metric, data=top_10_df, palette="viridis", ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    return fig

def plot_clusters(engagement_df):
    """
    Plot the distribution of users across engagement clusters.
    
    Args:
    - engagement_df (DataFrame): The dataframe with engagement metrics and assigned clusters.
    
    Returns:
    - fig: Matplotlib figure for the cluster plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='TotalTraffic', y='TotalSessionDuration', hue='Cluster', data=engagement_df, palette='Set1', ax=ax)
    ax.set_xlabel('Total Traffic (bytes)')
    ax.set_ylabel('Total Session Duration (seconds)')
    ax.set_title('User Clustering based on Engagement Metrics')
    return fig

def plot_histogram(df_engagement, metrics=['SessionFrequency', 'TotalSessionDuration', 'TotalTraffic']):
    """
    Plots histograms for the given engagement metrics.
    
    Args:
    - df_engagement (DataFrame): DataFrame containing the engagement metrics.
    - metrics (list): List of metrics to plot.
    
    Returns:
    - fig (matplotlib.figure.Figure): Matplotlib figure.
    """
    
    fig, axes = plt.subplots(1, len(metrics), figsize=(15, 5))
    for idx, metric in enumerate(metrics):
        sns.histplot(df_engagement[metric], bins=20, kde=True, ax=axes[idx])
        axes[idx].set_title(f'{metric} Distribution')
        axes[idx].set_xlabel(metric)
        axes[idx].set_ylabel('Frequency')
    
    plt.tight_layout()
    return fig

def plot_top_applications(df):
    """
    Plot the top 3 most used applications based on total traffic.
    
    Args:
    - df (DataFrame): DataFrame with aggregated application traffic for users.
    
    Returns:
    - fig (matplotlib.figure.Figure): Matplotlib figure for the top 3 applications.
    """
    
    app_traffic = df.sum(axis=0).sort_values(ascending=False).head(3)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=app_traffic.index, y=app_traffic.values, ax=ax)
    ax.set_title('Top 3 Most Used Applications')
    ax.set_ylabel('Total Traffic (Bytes)')
    ax.set_xlabel('Applications')
    return fig

def plot_kmeans_clusters(df_engagement):
    """
    Visualizes the K-Means clusters.
    
    Args:
    - df_engagement (DataFrame): DataFrame with cluster labels and metrics.
    
    Returns:
    - fig (matplotlib.figure.Figure): Matplotlib figure with K-Means clusters plotted.
    """
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_engagement, x='SessionFrequency', y='TotalTraffic', hue='Cluster', palette='viridis', s=100)
    plt.title('K-Means Clusters Based on Session Frequency and Total Traffic')
    plt.xlabel('Session Frequency')
    plt.ylabel('Total Traffic')
    plt.legend(title='Cluster')
    fig = plt.gcf()
    return fig