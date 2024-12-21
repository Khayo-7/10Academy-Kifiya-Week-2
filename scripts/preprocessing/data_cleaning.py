def drop_missing_data(dataframe, columns, how="any"):

    return dataframe.dropna(subset=columns, how=how, inplace=True)

def handle_missing_numerical(dataframe, numerical_columns):

    dataframe[numerical_columns] = dataframe[numerical_columns].fillna(dataframe[numerical_columns].mean())
    return dataframe

def handle_missing_categorical(dataframe, categorical_defaults):    
   
    return dataframe.fillna(value=categorical_defaults)

def treat_outliers(dataframe):

    numerical_columns = dataframe.select_dtypes(include=['number']).columns
    Q1 = dataframe[numerical_columns].quantile(0.25)
    Q3 = dataframe[numerical_columns].quantile(0.75)
    IQR = Q3 - Q1
    dataframe = dataframe[~((dataframe[numerical_columns] < (Q1 - 1.5 * IQR)) | (dataframe[numerical_columns] > (Q3 + 1.5 * IQR))).any(axis=1)]
    return dataframe

def clean_data(dataframe):

    print("Before cleaning:")
    print(dataframe.info())
    print(dataframe.describe())

    numerical_columns = dataframe.select_dtypes(include=['number']).columns
    # categorical_columns = dataframe.select_dtypes(include=['object']).columns
    categorical_columns = {
        'Bearer Id': 'Unknown',
        'IMSI': 'Unknown',
        'IMEI': 'Unknown'
    }

    # dataframe = drop_missing_data(dataframe, numerical_columns)
    dataframe.drop_duplicates(inplace=True)    
    # Handle missing values
    # dataframe.ffill(inplace=True)
    # dataframe.bfill(inplace=True)
    dataframe = handle_missing_numerical(dataframe, numerical_columns)
    dataframe = handle_missing_categorical(dataframe, categorical_columns)
    dataframe = treat_outliers(dataframe)

    print("After cleaning:")
    print(dataframe.info())
    print(dataframe.describe())

    print("Data cleaning completed.")
    return dataframe
