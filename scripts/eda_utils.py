import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def segment_users(dataframe, column, num_deciles):
    """
    Segment users into deciles based on a given column.

    Parameters:
    dataframe (pd.DataFrame): Input dataframe
    column (str): Column to segment users by
    num_deciles (int): Number of deciles to segment users into

    Returns:
    pd.DataFrame: Dataframe with added decile column
    """
    decile_column = f'{column}Decile'
    dataframe[decile_column] = pd.qcut(dataframe[column], num_deciles, labels=False)
    return dataframe

def compute_decile_summary(dataframe, decile_column, agg_columns, agg_functions):
    """
    Compute total data volume (DL + UL) per decile.

    Parameters:
    dataframe (pd.DataFrame): Input dataframe
    decile_column (str): Column to group by
    agg_columns (list): List of column names to aggregate
    agg_functions (list): List of aggregation functions

    Returns:
    pd.DataFrame: Dataframe with aggregated values
    """
    agg_dict = {col: func for col, func in zip(agg_columns, agg_functions)}
    decile_summary = dataframe.groupby(decile_column).agg(agg_dict)
    return decile_summary

def compute_dispersion_measures(dataframe, columns, functions):
    """
    Compute dispersion measures for a given dataframe.

    Parameters:
    dataframe (pd.DataFrame): Input dataframe
    columns (list): List of column names to compute dispersion for
    functions (list): List of dispersion functions

    Returns:
    pd.DataFrame: Dataframe with dispersion measures
    """
    return dataframe[columns].agg(functions)

def melt_dataframe(dataframe, app_columns):
    # Melt the application columns into rows

    return dataframe.melt(
        id_vars=['Bearer Id', 'Dur. (ms)', 'total_data_volume','Total DL (Bytes)','Total UL (Bytes)'],
        value_vars=app_columns,
        var_name='app_name',
        value_name='data_volume'
    )

def get_aggregate_dataframe(dataframe):
    # Aggregate per user and application
    
    return dataframe.groupby(['Bearer Id', 'app_name']).agg(
        number_of_sessions=('Dur. (ms)', 'count'),
        total_session_duration=('Dur. (ms)', 'sum'),
        total_download_data=( 'Total DL (Bytes)', 'sum'),
        total_upload_data=( 'Total UL (Bytes)', 'sum'),
        total_data_volume=('data_volume', 'sum')
    ).reset_index()


def get_dispersion_summary(dataframe):
    # Compute dispersion parameters for each quantitative variable

    numeric_dataframe = dataframe.select_dtypes(include='number')

    return pd.DataFrame({
        'Mean': numeric_dataframe.mean(),
        'Median': numeric_dataframe.median(),
        'Range': numeric_dataframe.max() - numeric_dataframe.min(),
        'Variance': numeric_dataframe.var(),
        'Std Dev': numeric_dataframe.std(),
        'IQR': numeric_dataframe.quantile(0.75) - numeric_dataframe.quantile(0.25)
    })


def apply_pca(dataframe, columns, n_components):
    """
    Apply PCA to a given dataframe.

    Parameters:
    dataframe (pd.DataFrame): Input dataframe
    columns (list): List of column names to apply PCA to
    n_components (int): Number of components for PCA

    Returns:
    pd.DataFrame: Dataframe with PCA results
    """

    pca = PCA(n_components=n_components)
    scaler = StandardScaler()
    X = dataframe[columns]
    X_scaled = scaler.fit_transform(X)

    principal_components = pca.fit_transform(X_scaled) # Apply PCA
    pca_dataframe = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)])
    
    return pca_dataframe, pca.explained_variance_ratio_
