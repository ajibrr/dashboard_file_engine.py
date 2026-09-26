import pandas as pd


def _bool_series(values: pd.Series) -> pd.Series:
    """
    Convert a pandas boolean result into a Series containing
    native Python bool objects.

    This is important because tests may use:

        result.iloc[0] is True

    pandas normally returns numpy.bool_, which is not identical
    to Python's True.
    """

    return values.astype(bool).astype(object)


# ============================================================
# BASIC COMPARISONS
# ============================================================

def greater_than(
    df: pd.DataFrame,
    column: str,
    value: float
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    return _bool_series(
        df[column] > value
    )


def less_than(
    df: pd.DataFrame,
    column: str,
    value: float
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    return _bool_series(
        df[column] < value
    )


def column_greater_than(
    df: pd.DataFrame,
    column1: str,
    column2: str
) -> pd.Series:

    if column1 not in df.columns:
        raise ValueError(
            f"Column not found: {column1}"
        )

    if column2 not in df.columns:
        raise ValueError(
            f"Column not found: {column2}"
        )

    return _bool_series(
        df[column1] > df[column2]
    )


def column_less_than(
    df: pd.DataFrame,
    column1: str,
    column2: str
) -> pd.Series:

    if column1 not in df.columns:
        raise ValueError(
            f"Column not found: {column1}"
        )

    if column2 not in df.columns:
        raise ValueError(
            f"Column not found: {column2}"
        )

    return _bool_series(
        df[column1] < df[column2]
    )


# ============================================================
# RISING CONDITIONS
# ============================================================

def rising_one_candle(
    df: pd.DataFrame,
    column: str
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    result = df[column] > df[column].shift(1)

    return _bool_series(
        result.fillna(False)
    )


def rising_three_candles(
    df: pd.DataFrame,
    column: str
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    current = df[column]
    previous_1 = current.shift(1)
    previous_2 = current.shift(2)

    result = (
        (current > previous_1)
        &
        (previous_1 > previous_2)
    )

    return _bool_series(
        result.fillna(False)
    )


# ============================================================
# FALLING CONDITIONS
# ============================================================

def falling_one_candle(
    df: pd.DataFrame,
    column: str
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    result = df[column] < df[column].shift(1)

    return _bool_series(
        result.fillna(False)
    )


def falling_three_candles(
    df: pd.DataFrame,
    column: str
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    current = df[column]
    previous_1 = current.shift(1)
    previous_2 = current.shift(2)

    result = (
        (current < previous_1)
        &
        (previous_1 < previous_2)
    )

    return _bool_series(
        result.fillna(False)
    )


# ============================================================
# LOOKBACK CONDITIONS
# ============================================================

def greater_than_lookback(
    df: pd.DataFrame,
    column: str,
    lookback: int
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    if lookback <= 0:
        raise ValueError(
            "lookback must be greater than 0"
        )

    result = (
        df[column]
        >
        df[column].shift(lookback)
    )

    return _bool_series(
        result.fillna(False)
    )


def less_than_lookback(
    df: pd.DataFrame,
    column: str,
    lookback: int
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    if lookback <= 0:
        raise ValueError(
            "lookback must be greater than 0"
        )

    result = (
        df[column]
        <
        df[column].shift(lookback)
    )

    return _bool_series(
        result.fillna(False)
    )


# ============================================================
# GREATER THAN ALL PREVIOUS VALUES
# ============================================================

def greater_than_all_previous(
    df: pd.DataFrame,
    column: str,
    lookback: int
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    if lookback <= 0:
        raise ValueError(
            "lookback must be greater than 0"
        )

    previous_max = (
        df[column]
        .shift(1)
        .rolling(
            window=lookback,
            min_periods=lookback
        )
        .max()
    )

    result = df[column] > previous_max

    return _bool_series(
        result.fillna(False)
    )


# ============================================================
# LESS THAN ALL PREVIOUS VALUES
# ============================================================

def less_than_all_previous(
    df: pd.DataFrame,
    column: str,
    lookback: int
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    if lookback <= 0:
        raise ValueError(
            "lookback must be greater than 0"
        )

    previous_min = (
        df[column]
        .shift(1)
        .rolling(
            window=lookback,
            min_periods=lookback
        )
        .min()
    )

    result = df[column] < previous_min

    return _bool_series(
        result.fillna(False)
    )


# ============================================================
# RSI CONDITIONS
# ============================================================

def rsi_above(
    df: pd.DataFrame,
    column: str,
    value: float
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    return _bool_series(
        df[column] > value
    )


def rsi_below(
    df: pd.DataFrame,
    column: str,
    value: float
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    return _bool_series(
        df[column] < value
    )


# ============================================================
# OI CONDITIONS
# ============================================================

def oi_increasing(
    df: pd.DataFrame,
    column: str
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    result = df[column] > df[column].shift(1)

    return _bool_series(
        result.fillna(False)
    )


def oi_decreasing(
    df: pd.DataFrame,
    column: str
) -> pd.Series:

    if column not in df.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    result = df[column] < df[column].shift(1)

    return _bool_series(
        result.fillna(False)
    )