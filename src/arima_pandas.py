import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import sys


def parse_data(readings):
    timestamps = []
    prices = []

    # Parse the input data
    for data in readings:
        timestamp, price = data.split('\t')
        timestamps.append(pd.to_datetime(timestamp))

        if 'Missing' in price:
            prices.append(np.nan)  # Use np.nan to signify missing data
        else:
            prices.append(float(price))

    return pd.DataFrame({'Timestamp': timestamps, 'Price': prices}).set_index('Timestamp')


def interpolate_with_arima(df):
    # Fill missing values using ARIMA model predictions
    model = ARIMA(df['Price'].astype(float), order=(1, 1, 1))
    model_fit = model.fit()

    # Predict and fill missing values
    df['Price'] = model_fit.predict(start=df.index[0], end=df.index[-1], typ='levels')

    return df


def output_results(df):
    # Print the interpolated prices
    for timestamp, row in df.iterrows():
        if pd.isna(row['OriginalPrice']) and not pd.isna(row['Price']):  # Only print filled missing values
            print(f"{timestamp.strftime('%m/%d/%Y %H:%M:%S')}\t{row['Price']:.2f}")


if __name__ == "__main__":
    readings_count = int(input().strip())
    readings = [input().strip() for _ in range(readings_count)]

    data_df = parse_data(readings)
    data_df['OriginalPrice'] = data_df['Price']  # Preserve the original data for comparison
    interpolated_data = interpolate_with_arima(data_df)
    output_results(interpolated_data)
