def calcMissing(readings):
    timestamps = []
    prices = []
    missing = {}

    # Parse the input data
    for index, data in enumerate(readings):
        timestamp, price = data.split('\t')
        timestamps.append(timestamp)

        # Identify missing prices and mark them with None
        if 'Missing' in price:
            prices.append(None)
            missing[index] = price  # Store the index and label of missing prices
        else:
            prices.append(float(price))

    # Interpolate missing prices
    for i in range(len(prices)):
        if prices[i] is None:
            # Find previous and next known prices for interpolation
            prev, next = i - 1, i + 1
            while prices[prev] is None and prev >= 0:
                prev -= 1
            while next < len(prices) and prices[next] is None:
                next += 1

            if prev >= 0 and next < len(prices):
                prices[i] = prices[prev] + (prices[next] - prices[prev]) * ((i - prev) / (next - prev))
            elif prev >= 0:
                prices[i] = prices[prev]
            elif next < len(prices):
                prices[i] = prices[next]

    for index in sorted(missing):
        print(f"{prices[index]:.2f}")


if __name__ == "__main__":
    readings_count = int(input().strip())
    readings = []

    for _ in range(readings_count):
        readings_item = input().strip()
        readings.append(readings_item)

    calcMissing(readings)
