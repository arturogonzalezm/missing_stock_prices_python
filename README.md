# Missing Stock Prices - HackerRank Challenge

A time series of a stock's highest price during a trading day at the New York Stock Exchange is provided to you. Each test case has day's highest prices missing for certain days. Analyze the data to identify the missing price for those particular days.

## Input Format

- The first line contains an integer `N`, which represents the number of rows of data to follow.
- Each of the next `N` rows contains data with the following columns:
  - A **time-stamp** in the first column.
  - The **day's highest price** for the stock in the second column.

Columns are delimited by a tab. Each input file exactly contains twenty rows where the day's highest price is missing, marked as `"Missing_1"`, `"Missing_2"`, ..., `"Missing_20"`. These missing records are randomly dispersed among the rows.

## Output Format

The output should contain exactly twenty rows, each containing your predicted value for each of the missing values (`Missing_1`, `Missing_2`, ..., `Missing_20`) in that order.

## Scoring

The scoring will be based on the mean of the magnitude of the percentage difference by comparing your expected answers with the actual stock price high for each missing record across all test cases. The difference is calculated as follows:

```text
d = Summation of abs((expected price - computed price)/expected price) x 100
```

## Scoring Criteria

$$
50 \times \max(2 - d, 0)
$$

```latex
\begin{align*}
50 \times \max(2 - d, 0)
\end{align*}
```



