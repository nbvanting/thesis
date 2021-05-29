from tensorflow.keras.preprocessing import timeseries_dataset_from_array
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd
import numpy as np
import datetime as dt


def create_datasets(dataframe, split, steps, lookback, horizon, batch_size, scaler='standard'):
    # Split method
    train_split = int(split * dataframe.shape[0])
    val_split = int((split+0.1) * dataframe.shape[0])

    train = dataframe.iloc[:train_split]
    val = dataframe.iloc[train_split:val_split]
    test = dataframe.iloc[val_split:]

    # Scaler
    if scaler == 'standard':
        X_scaler = StandardScaler()
        y_scaler = StandardScaler()
    elif scaler == 'minmax':
        X_scaler = MinMaxScaler()
        y_scaler = MinMaxScaler()
    else:
        print("Please specify one of 'standard' or 'minmax' to scaler parameter.")
    
    # Training
    start = lookback + horizon
    end = start + train_split

    X_train = train.values
    y_train = dataframe.iloc[start:end][['Value']]

    X_train = X_scaler.fit_transform(X_train)
    y_train = y_scaler.fit_transform(y_train)

    # Validation
    x_end = len(val) - lookback - horizon
    y_val_start = train_split + lookback + horizon

    X_val = val.iloc[:x_end]
    y_val = dataframe.iloc[y_val_start:y_val_start+x_end][['Value']]

    X_val = X_scaler.transform(X_val)
    y_val = y_scaler.transform(y_val)

    # Test
    x_end = len(test) - lookback - horizon
    y_test_start = val_split + lookback + horizon

    X_test = test.iloc[:x_end]
    y_test = dataframe.iloc[y_test_start:y_test_start+x_end][['Value']]

    X_test = X_scaler.transform(X_test)
    y_test = y_scaler.transform(y_test)

    # Batch Sequence Generators
    sequence_length = int(lookback/steps)

    dataset_train = timeseries_dataset_from_array(
        X_train, y_train,
        sequence_length=sequence_length,
        sampling_rate=steps,
        batch_size=batch_size,
        shuffle=True
    )

    dataset_val = timeseries_dataset_from_array(
        X_val, y_val,
        sequence_length=sequence_length,
        sampling_rate=steps,
        batch_size=batch_size,
        shuffle=True
    )    

    dataset_test = timeseries_dataset_from_array(
        X_test, y_test,
        sequence_length=sequence_length,
        sampling_rate=steps,
        batch_size=batch_size,
        shuffle=False
    )    

    return dataset_train, dataset_val, dataset_test


def ts_offset_split(dataframe, steps, lookback, horizon, batch_size, scaler='standard'):
    '''
    This pipeline function returns 3 Keras Timeseries Dataset Objects: train, validation, and test.
    The function first splits the data with the offset split method every 8th day.
    Afterwards the data is scaled by either using the StandardScaler or MinMaxScaler from SciKit library.
    Finally the dataframe is split using the lookback and horizon parameters. 
    '''
    # Offset 8th Day Split
    start = 0 
    end = 168
    offset = 24
    training = []
    validation = []

    for i in range(int((365+366)/8)):

        train = dataframe.iloc[start:end]
        val = dataframe.iloc[end:end+offset]
        training.append(train)
        validation.append(val)

        start += 192
        end += 192
    
    # Decide Splits for sets
    train = pd.concat(training)
    
    val = pd.concat(validation)
    
    train = train.append(dataframe[(dataframe.index.date > val.index.max()) & (dataframe.index.date < dt.date(2021,1,1))])

    test = dataframe[dataframe.index.date >= dt.date(2021,1,1)]
    
    tmpdf = pd.concat([train,val,test])

    # Scaler
    if scaler == 'standard':
        X_scaler = StandardScaler()
        y_scaler = StandardScaler()
    elif scaler == 'minmax':
        X_scaler = MinMaxScaler()
        y_scaler = MinMaxScaler()
    elif scaler == None:
        print("Data has not been scaled.")
    else: 
        print('Please specify scaler: standard, minmax, or None')

    # Training Split
    start = lookback + horizon
    end = start + train.shape[0]

    X_train = train.values
    y_train = tmpdf.iloc[start:end][['Value']]

    if scaler != None:
        X_train = X_scaler.fit_transform(X_train)
        y_train = y_scaler.fit_transform(y_train)

    # Validation Split
    x_end = len(val) - lookback - horizon
    y_val_start = train.shape[0] + lookback + horizon

    X_val = val.iloc[:x_end]
    y_val = tmpdf.iloc[y_val_start:y_val_start+x_end][['Value']]

    if scaler != None:
        X_val = X_scaler.transform(X_val)
        y_val = y_scaler.transform(y_val)

    # Test Split
    x_end = len(test) - lookback - horizon
    y_test_start = (train.shape[0] + val.shape[0]) + lookback + horizon

    X_test = test.iloc[:x_end]
    y_test = tmpdf.iloc[y_test_start:y_test_start+x_end][['Value']]

    if scaler != None:
        X_test = X_scaler.transform(X_test)
        y_test = y_scaler.transform(y_test)

    # Batch Sequence Generators
    sequence_length = int(lookback/steps)

    dataset_train = timeseries_dataset_from_array(
        X_train, y_train,
        sequence_length=sequence_length,
        sampling_rate=steps,
        batch_size=batch_size,
        shuffle=True
    )

    dataset_val = timeseries_dataset_from_array(
        X_val, y_val,
        sequence_length=sequence_length,
        sampling_rate=steps,
        batch_size=batch_size,
        shuffle=True
    )    

    dataset_test = timeseries_dataset_from_array(
        X_test, y_test,
        sequence_length=sequence_length,
        sampling_rate=steps,
        batch_size=batch_size,
        shuffle=False
    )    

    return dataset_train, dataset_val, dataset_test