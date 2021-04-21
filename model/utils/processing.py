from tensorflow.keras.preprocessing import timeseries_dataset_from_array
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd
import numpy as np


def create_datasets(dataframe, split, steps, lookback, horizon, batch_size, scaler='standard'):
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
        batch_size=batch_size
    )

    dataset_val = timeseries_dataset_from_array(
        X_val, y_val,
        sequence_length=sequence_length,
        sampling_rate=steps,
        batch_size=batch_size
    )    

    dataset_test = timeseries_dataset_from_array(
        X_test, y_test,
        sequence_length=sequence_length,
        sampling_rate=steps,
        batch_size=batch_size
    )    

    return dataset_train, dataset_val, dataset_test