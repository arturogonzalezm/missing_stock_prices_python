import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
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
            missing_indices.append(index)  # Keep track of missing data indices
        else:
            prices.append(float(price))

    return pd.DataFrame({'Timestamp': timestamps, 'Price': prices}).set_index('Timestamp'), missing_indices


def prepare_features(df):
    # Creating time-related features from the timestamp
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df['Day'] = df.index.day
    df['DayOfWeek'] = df.index.dayofweek
    return df


def gradient_boosting_interpolation(df, missing_indices):
    # Prepare features
    df = prepare_features(df)

    # Separate known and unknown data
    known_data = df.dropna()
    unknown_indices = df.index[missing_indices]  # This assumes missing_indices refers directly to the DataFrame indices

    # Fit Gradient Boosting model on known data
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(known_data.drop(['Price'], axis=1), known_data['Price'])

    # Predict the missing prices and update using .loc to avoid SettingWithCopyWarning
    predicted_prices = model.predict(df.loc[unknown_indices].drop(['Price'], axis=1))
    df.loc[unknown_indices, 'Price'] = predicted_prices  # Correct method to avoid potential issues

    return df.loc[unknown_indices, 'Price']


def output_results(prices):
    # Print the interpolated prices
    for price in prices:
        print(f"{price:.2f}")


if __name__ == "__main__":
    readings_count = int(input().strip())
    readings = [input().strip() for _ in range(readings_count)]

    data_df, missing_indices = parse_data(readings)
    predicted_prices = gradient_boosting_interpolation(data_df, missing_indices)
    output_results(predicted_prices)
