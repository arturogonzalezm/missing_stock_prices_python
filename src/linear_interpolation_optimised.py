def parse_readings(readings):
    timestamps = []
    prices = []
    missing_indices = []

    for index, data in enumerate(readings):
        timestamp, price = data.split('\t')
        timestamps.append(timestamp)

        if 'Missing' in price:
            prices.append(None)
            missing_indices.append(index)
        else:
            prices.append(float(price))

    return timestamps, prices, missing_indices


def interpolate_prices(prices):
    n = len(prices)
    for i in range(n):
        if prices[i] is None:
            # Find the nearest known prices before and after the missing price
            prev = i - 1
            while prev >= 0 and prices[prev] is None:
                prev -= 1
            next = i + 1
            while next < n and prices[next] is None:
                next += 1

            # Calculate the interpolated price
            if prev >= 0 and next < n:
                prices[i] = prices[prev] + (prices[next] - prices[prev]) * ((i - prev) / (next - prev))
            elif prev >= 0:
                prices[i] = prices[prev]  # No next known price, extend the last known value
            elif next < n:
                prices[i] = prices[next]  # No previous known price, extend the next known value


def print_missing_prices(prices, missing_indices):
    for index in missing_indices:
        print(f"{prices[index]:.2f}")


def calcMissing(readings):
    timestamps, prices, missing_indices = parse_readings(readings)
    interpolate_prices(prices)
    print_missing_prices(prices, missing_indices)


if __name__ == "__main__":
    readings_count = int(input().strip())
    readings = []

    for _ in range(readings_count):
        readings_item = input().strip()
        readings.append(readings_item)

    calcMissing(readings)
