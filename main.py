# Import necessary modules for the various interpolation methods

import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from scipy.interpolate import interp1d


# Function to parse and prepare data
def parse_data(file_path):
    timestamps = []
    prices = []
    missing_indices = []

    with open(file_path, 'r') as file:
        next(file)  # Skip the first line if it contains headers or the count of rows
        for index, data in enumerate(file):
            data = data.strip()
            try:
                timestamp, price = data.split('\t')
                timestamps.append(pd.to_datetime(timestamp))

                if 'Missing' in price:
                    prices.append(np.nan)
                    missing_indices.append(index)
                else:
                    prices.append(float(price))
            except ValueError:
                print(f"Error processing line: {data}")  # Debugging help

    df = pd.DataFrame({'Timestamp': timestamps, 'Price': prices}).set_index('Timestamp')
    return df, missing_indices


# Function to prepare features for ML models
def prepare_features(df):
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df['Day'] = df.index.day
    df['DayOfWeek'] = df.index.dayofweek
    return df


# Different interpolation methods
def arima_interpolation(df):
    model = ARIMA(df['Price'].astype(float), order=(1, 1, 1))
    model_fit = model.fit()
    df['Price'] = model_fit.predict(start=df.index[0], end=df.index[-1], typ='levels')
    return df


def gradient_boosting_interpolation(df, missing_indices):
    df = prepare_features(df)
    known_data = df.dropna()
    unknown_indices = df.index[missing_indices]
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(known_data.drop(['Price'], axis=1), known_data['Price'])
    predicted_prices = model.predict(df.loc[unknown_indices].drop(['Price'], axis=1))
    df.loc[unknown_indices, 'Price'] = predicted_prices
    return df


def random_forest_interpolation(df, missing_indices):
    df = prepare_features(df)
    train = df.dropna()
    test_indices = df.index[missing_indices]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train.drop(['Price'], axis=1), train['Price'])

    # Predict missing values
    predicted_prices = model.predict(df.loc[test_indices].drop(['Price'], axis=1))
    df.loc[test_indices, 'Price'] = predicted_prices  # Set values using .loc to avoid SettingWithCopyWarning
    return df.loc[test_indices]


def spline_interpolation(df, missing_indices):
    times = df.index.astype(np.int64)
    valid_times = times[~df['Price'].isnull()]
    valid_prices = df['Price'].dropna().to_numpy()
    spline_interpolator = interp1d(valid_times, valid_prices, kind='cubic', fill_value='extrapolate')
    interpolated_prices = spline_interpolator(times)
    df.loc[df['Price'].isnull(), 'Price'] = interpolated_prices[df['Price'].isnull()]
    return df


# Function to perform linear interpolation
def linear_interpolation(df):
    # Perform linear interpolation at the missing points
    df['Price'] = df['Price'].interpolate(method='linear')
    return df


def main():
    data_path = 'data/input/input00.txt'
    # Parsing the data
    data_df, missing_indices = parse_data(data_path)

    # Applying different interpolation methods
    arima_df = arima_interpolation(data_df.copy())
    gradient_df = gradient_boosting_interpolation(data_df.copy(), missing_indices)
    random_forest_df = random_forest_interpolation(data_df.copy(), missing_indices)
    spline_df = spline_interpolation(data_df.copy(), missing_indices)
    interpolated_df = linear_interpolation(data_df.copy())

    hackerrank_data = []
    with open('data/output/output00.txt', 'r') as file:
        hackerrank_data = [float(line.strip()) for line in file]

    # Extract interpolated prices for missing indices
    results = pd.DataFrame({
        'ARIMA': arima_df.iloc[missing_indices]['Price'].values,
        'Gradient Boosting': gradient_df.iloc[missing_indices]['Price'].values,
        'Random Forest': random_forest_df['Price'].values,
        'Spline': spline_df.iloc[missing_indices]['Price'].values,
        'Linear': interpolated_df.iloc[missing_indices]['Price'].values
    }, index=arima_df.index[missing_indices])

    # Assuming 'results' DataFrame is indexed properly to align with the hackerrank data
    results['hackerrank'] = hackerrank_data
    return results


if __name__ == '__main__':
    print(main())
