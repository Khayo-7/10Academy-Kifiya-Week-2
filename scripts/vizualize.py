import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Disable interactive mode for matplotlib
# plt.ioff()

def plot_data(data, plot_type, x=None, y=None, **kwargs):
    """
    A general-purpose plotting function for Streamlit and Jupyter with explicit figure return.

    Args:
        data (pd.Data): The data to plot.
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
        sns.histplot(data[x], 
                     bins=kwargs.get('bins', 10), 
                     kde=kwargs.get('kde', False), 
                     color=kwargs.get('color', 'skyblue'), 
                     edgecolor=kwargs.get('edgecolor', 'black'),
                     ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', 'Values'))
        ax.set_ylabel(kwargs.get('ylabel', 'Frequency'))

    elif plot_type == 'boxplot':
        sns.boxplot(x=data[x], y=data[y] if y else None, ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', y) if y else 'Values')

    elif plot_type == 'violinplot':
        sns.violinplot(x=data[x] if x else None, y=data[y] if y else None, ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', y) if y else 'Values')

    elif plot_type == 'scatter':
        # sns.scatterplot(data=data[x], x=x, y=y, ax=ax)
        ax.scatter(data[x], data[y], 
                   c=kwargs.get('color', 'blue'), 
                   alpha=kwargs.get('alpha', 0.5))
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', y))

    elif plot_type == 'heatmap':
        # numeric_data = data.corr()  # Default is correlation heatmap
        numeric_data = data.applymap(lambda x: pd.to_numeric(x, errors='coerce'))
        sns.heatmap(numeric_data, 
                    annot=kwargs.get('annot', True), 
                    cmap=kwargs.get('cmap', 'coolwarm'), 
                    fmt=kwargs.get('fmt', ".2f"), 
                    linewidths=kwargs.get('linewidths', 0.5),
                    ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', ''))
        ax.set_ylabel(kwargs.get('ylabel', ''))

    elif plot_type == 'bar':
        data[x].value_counts().plot(kind='bar', 
                                         color=kwargs.get('color', 'lightgreen'), 
                                         edgecolor=kwargs.get('edgecolor', 'black'),
                                         ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', 'Frequency'))

    elif plot_type == 'kde':
        sns.kdeplot(data[x], shade=kwargs.get('shade', True), ax=ax)
        ax.set_xlabel(kwargs.get('xlabel', x))
    
    ax.set_title(kwargs.get('title', ''))
    plt.xticks(rotation=kwargs.get('xticks_rotation', 0))
    
    return fig
    # return plt.gcf()

def plot_histogram(data, columns, bins=15, title="Histograms", orientation='v', figsize=(12, 8)):
    """
    Plots histograms for the specified columns.
    
    Args:
        data (Data): Dataset.
        columns (list): Columns to plot.
        bins (int): Number of bins for the histogram.
        title (str): Overall title for the histograms.
        figsize (tuple): Size of the figure.
    
    Returns:
        plt.Figure: Matplotlib figure object.
    """
    if orientation == 'h':
        fig, axes = plt.subplots(1, len(columns), figsize=figsize)
    else:
        fig, axes = plt.subplots(len(columns), 1, figsize=figsize)

    axes = axes if len(columns) > 1 else [axes]
    for col, ax in zip(columns, axes):
        data[col].plot(kind='hist', bins=bins, ax=ax, edgecolor='black')
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel(col)
    
    fig.suptitle(title)
    plt.tight_layout()
    
    return fig

def plot_boxplot(data, columns, title="Boxplots", figsize=(12, 6)):
    """
    Plots boxplots for the specified columns.
    
    Args:
        data (Data): Dataset.
        columns (list): Columns to plot.
        title (str): Overall title for the boxplots.
        figsize (tuple): Size of the figure.
    
    Returns:
        plt.Figure: Matplotlib figure object.
    """
    fig, axes = plt.subplots(1, len(columns), figsize=figsize)
    axes = axes if len(columns) > 1 else [axes]
    for col, ax in zip(columns, axes):
        sns.boxplot(y=data[col], ax=ax)
        ax.set_title(f'Boxplot for {col}')
    fig.suptitle(title)
    return fig

def plot_correlation_matrix(data, columns, title="Correlation Matrix", figsize=(8, 6)):
    """
    Plots a heatmap for the correlation matrix of specified columns.
    
    Args:
        data (Data): Dataset.
        columns (list): Columns to include in the correlation matrix.
        title (str): Title of the heatmap.
        figsize (tuple): Size of the figure.
    
    Returns:
        plt.Figure: Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=figsize)
    correlation = data[columns].corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title(title)
    return fig

def plot_bar(data, title, xlabel=None, ylabel=None, rotation=45, figsize=(10, 6), orientation='v'):

    fig, ax = plt.subplots(figsize=figsize)
    
    sns.barplot(data=data, ax=ax, orient=orientation)
    ax.set_title(title)
    ax.set_xlabel(xlabel or "")
    ax.set_ylabel(ylabel or "")
    plt.xticks(rotation=rotation)
    plt.tight_layout()
   
    return fig

def plot_pie(data, labels_column, values_column, title):
    
    fig, ax = plt.subplots(figsize=(8, 8))
    # data.plot.pie(y=values_column, labels=None, autopct="%1.1f%%", title=title, ax=ax)
    wedges, _, _ = ax.pie(data[values_column], labels=None, autopct="%1.1f%%")
    ax.legend(wedges, data[labels_column], title=title)
    ax.set_ylabel("")
    plt.tight_layout()
    
    return fig

def plot_stacked_bar(data, x_column, categories, title):

    fig, ax = plt.subplots(figsize=(12, 8))
    data = data[categories + [x_column]]
    data.plot(kind="bar", x=x_column, stacked=True, ax=ax, colormap="coolwarm")
    ax.set_title(title)
    
    return fig


def plot_scatter(data, x_column, y_column, title="Scatter Plot", xlabel='', ylabel='', color="blue", palette='viridis', figsize=(8, 6), s=100):
    """
    Plots a scatter plot for two variables.
    
    Args:
        data (Data): Dataset.
        x (str): X-axis variable.
        y (str): Y-axis variable.
        title (str): Title of the scatter plot.
        figsize (tuple): Size of the figure.
    
    Returns:
        plt.Figure: Matplotlib figure object.
    """

    fig, ax = plt.subplots(figsize=figsize)   

    sns.scatterplot(data=data, x=x_column, y=y_column, ax=ax, color=color, palette=palette, alpha=0.6, s=s)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    return fig

def plot_scatter_outliers(data, x_column, y_column, xlabel, ylabel, title="Outliers Scatter Plot", outliers=None):
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot for normal points
    sns.scatterplot(data=data, x=x_column, y=y_column, color='blue', alpha=0.6, label="Users", ax=ax)
    
    # Highlight outliers
    if outliers is not None:
        for key, value in outliers.items():
            if key == "Sessions":
                sns.scatterplot(data=value, x=x_column, y=y_column, color="red", label=f"Outliers - {key}", ax=ax)
            elif key == "Data":
                sns.scatterplot(data=value, x=x_column, y=y_column, color="green", label=f"Outliers - {key}", ax=ax)
    
    # Set labels and title
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(alpha=0.5)
    
    return fig
