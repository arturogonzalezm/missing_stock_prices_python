import numpy as np
from scipy.interpolate import interp1d
import pandas as pd


def calcMissing(readings):
    timestamps = []
    prices = []
    missing_indices = []

    # Parse the input data
    for index, data in enumerate(readings):
        timestamp, price = data.split('\t')
        timestamps.append(timestamp)

        if 'Missing' in price:
            prices.append(np.nan)  # Use NaN for missing data to facilitate interpolation
            missing_indices.append(index)
        else:
            prices.append(float(price))

    # Convert lists to numpy arrays for interpolation
    times = pd.to_datetime(timestamps).astype(np.int64)  # Convert timestamps to int64 for calculations

    # Prepare data for interpolation
    valid_times = times[~np.isnan(prices)]
    valid_prices = np.array(prices)[~np.isnan(prices)]

    # Create a spline interpolation model
    # 'slinear', 'quadratic' or 'cubic' for different smoothness
    spline_interpolator = interp1d(valid_times, valid_prices, kind='cubic', fill_value='extrapolate')

    # Interpolate missing prices
    interpolated_prices = spline_interpolator(times)

    # Output the interpolated results for the missing indices
    for index in missing_indices:
        print(f"{timestamps[index]}\t{interpolated_prices[index]:.2f}")


if __name__ == "__main__":
    readings_count = int(input().strip())
    readings = [input().strip() for _ in range(readings_count)]
    calcMissing(readings)
