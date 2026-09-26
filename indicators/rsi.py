import pandas as pd


def calculate_rsi(
    series: pd.Series,
    period: int = 14
) -> pd.Series:

    if period <= 0:
        raise ValueError(
            "RSI period must be greater than 0"
        )

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (
        100 / (1 + rs)
    )

    return rsi