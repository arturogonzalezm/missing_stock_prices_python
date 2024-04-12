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

The expression $$50 \times \max(2 - d, 0)$$ is a mathematical formula used in various contexts, often for scoring or evaluating performance based on a deviation measure 'd'. Here's a breakdown of each part of this formula:

- **50**: This is a constant multiplier used to scale the result of the function to a desired range or magnitude.

- **\(\max(2 - d, 0)\)**: This is the key function in the expression. It's the maximum function which compares two values and returns the larger of the two. In this case, it compares \(2 - d\) and \(0\).

  - **\(2 - d\)**: Here, \(d\) represents a deviation or error from a target or expected value. \(2 - d\) calculates a value that decreases as \(d\) increases. In many scoring systems, \(d\) could represent an error rate or a percentage difference, and the number 2 is a threshold value.
  
  - **0**: This ensures that the expression does not return a negative number. If \(d\) exceeds 2, making \(2 - d\) negative, the \(\max\) function will return 0.

**Putting it together:**

- When \(d\) (the deviation) is less than or equal to 2, \(2 - d\) will be positive and therefore \(50 \times \max(2 - d, 0)\) will yield a scaled positive score based on how much smaller \(d\) is than 2.

- When \(d\) is greater than 2, \(2 - d\) becomes negative, and \(\max(2 - d, 0)\) results in 0. Consequently, \(50 \times 0\) is 0, reflecting a failure to stay within the acceptable deviation range.

**In summary**, this formula is used to calculate a score that decreases with an increase in the deviation \(d\) beyond a set point (2 in this case), down to a minimum score of 0. It’s commonly used in contexts where there's a penalty for exceeding a certain error threshold, ensuring scores are non-negative.


$$
50 \times \max(2 - d, 0)
$$




