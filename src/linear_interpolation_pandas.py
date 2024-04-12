import pandas as pd
import numpy as np


def calcMissing(readings):
    data = {'timestamp': [], 'price': []}
    missing_indices = {}
    for i, line in enumerate(readings):
        parts = line.split('\t')
        timestamp, price = parts[0], parts[1]
        data['timestamp'].append(timestamp)

        if "Missing" in price:
            data['price'].append(np.nan)
            missing_indices[price] = i
        else:
            data['price'].append(float(price))

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    df['price'] = df['price'].interpolate(method='time')

    sorted_indices = sorted(missing_indices.items(), key=lambda x: x[0])
    for _, idx in sorted_indices:
        print(f"{df.iloc[idx]['price']:.2f}")


if __name__ == "__main__":
    readings_count = int(input().strip())
    readings = []

    for _ in range(readings_count):
        readings_item = input().strip()
        readings.append(readings_item)

    calcMissing(readings)
