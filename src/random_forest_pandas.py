import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import sys


def parse_data(readings):
    timestamps = []
    prices = []
    missing_indices = []

    # Parse the input data
    for index, data in enumerate(readings):
        timestamp, price = data.split('\t')
        timestamps.append(pd.to_datetime(timestamp))

        if 'Missing' in price:
            prices.append(np.nan)
            missing_indices.append(index)  # Track indices of missing prices
        else:
            prices.append(float(price))

    return pd.DataFrame({'Timestamp': timestamps, 'Price': prices}).set_index('Timestamp'), missing_indices


def prepare_features(df):
    # Extract features from the timestamp
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df['Day'] = df.index.day
    df['DayOfWeek'] = df.index.dayofweek
    return df


def random_forest_interpolation(df, missing_indices):
    # Prepare features
    df = prepare_features(df)

    # Separate known and unknown data
    train = df.dropna()
    test = df.iloc[missing_indices]

    # Fit model on known data
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train.drop(['Price'], axis=1), train['Price'])

    # Predict missing values
    predicted_prices = model.predict(test.drop(['Price'], axis=1))
    test['Price'] = predicted_prices

    return test['Price']


def output_results(prices):
    # Print the interpolated prices
    for price in prices:
        print(f"{price:.2f}")


if __name__ == "__main__":
    readings_count = int(input().strip())
    readings = [input().strip() for _ in range(readings_count)]

    data_df, missing_indices = parse_data(readings)
    predicted_prices = random_forest_interpolation(data_df, missing_indices)
    output_results(predicted_prices)
