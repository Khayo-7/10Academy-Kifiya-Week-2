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
