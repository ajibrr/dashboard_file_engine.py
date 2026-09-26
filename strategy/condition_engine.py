import pandas as pd

from data.condition import (
    greater_than,
    less_than,
    column_greater_than,
    column_less_than,
    rising_one_candle,
    rising_three_candles,
    falling_one_candle,
    falling_three_candles,
    greater_than_lookback,
    less_than_lookback,
    greater_than_all_previous,
    less_than_all_previous,
    rsi_above,
    rsi_below,
    oi_increasing,
    oi_decreasing,
)


class ConditionEngine:

    # ========================================================
    # BASIC COMPARISONS
    # ========================================================

    @staticmethod
    def greater_than(
        df: pd.DataFrame,
        column: str,
        value: float
    ) -> pd.Series:

        return greater_than(
            df,
            column,
            value
        )

    @staticmethod
    def less_than(
        df: pd.DataFrame,
        column: str,
        value: float
    ) -> pd.Series:

        return less_than(
            df,
            column,
            value
        )

    @staticmethod
    def column_greater_than(
        df: pd.DataFrame,
        column1: str,
        column2: str
    ) -> pd.Series:

        return column_greater_than(
            df,
            column1,
            column2
        )

    @staticmethod
    def column_less_than(
        df: pd.DataFrame,
        column1: str,
        column2: str
    ) -> pd.Series:

        return column_less_than(
            df,
            column1,
            column2
        )

    # ========================================================
    # RISING
    # ========================================================

    @staticmethod
    def rising_one_candle(
        df: pd.DataFrame,
        column: str
    ) -> pd.Series:

        return rising_one_candle(
            df,
            column
        )

    @staticmethod
    def rising_three_candles(
        df: pd.DataFrame,
        column: str
    ) -> pd.Series:

        return rising_three_candles(
            df,
            column
        )

    # ========================================================
    # FALLING
    # ========================================================

    @staticmethod
    def falling_one_candle(
        df: pd.DataFrame,
        column: str
    ) -> pd.Series:

        return falling_one_candle(
            df,
            column
        )

    @staticmethod
    def falling_three_candles(
        df: pd.DataFrame,
        column: str
    ) -> pd.Series:

        return falling_three_candles(
            df,
            column
        )

    # ========================================================
    # LOOKBACK
    # ========================================================

    @staticmethod
    def greater_than_lookback(
        df: pd.DataFrame,
        column: str,
        lookback: int
    ) -> pd.Series:

        return greater_than_lookback(
            df,
            column,
            lookback
        )

    @staticmethod
    def less_than_lookback(
        df: pd.DataFrame,
        column: str,
        lookback: int
    ) -> pd.Series:

        return less_than_lookback(
            df,
            column,
            lookback
        )

    # ========================================================
    # ALL PREVIOUS
    # ========================================================

    @staticmethod
    def greater_than_all_previous(
        df: pd.DataFrame,
        column: str,
        lookback: int
    ) -> pd.Series:

        return greater_than_all_previous(
            df,
            column,
            lookback
        )

    @staticmethod
    def less_than_all_previous(
        df: pd.DataFrame,
        column: str,
        lookback: int
    ) -> pd.Series:

        return less_than_all_previous(
            df,
            column,
            lookback
        )

    # ========================================================
    # RSI
    # ========================================================

    @staticmethod
    def rsi_above(
        df: pd.DataFrame,
        column: str,
        value: float
    ) -> pd.Series:

        return rsi_above(
            df,
            column,
            value
        )

    @staticmethod
    def rsi_below(
        df: pd.DataFrame,
        column: str,
        value: float
    ) -> pd.Series:

        return rsi_below(
            df,
            column,
            value
        )

    # ========================================================
    # OI
    # ========================================================

    @staticmethod
    def oi_increasing(
        df: pd.DataFrame,
        column: str
    ) -> pd.Series:

        return oi_increasing(
            df,
            column
        )

    @staticmethod
    def oi_decreasing(
        df: pd.DataFrame,
        column: str
    ) -> pd.Series:

        return oi_decreasing(
            df,
            column
        )

    # ========================================================
    # COMBINATION
    # ========================================================

    @staticmethod
    def all_conditions(
        *conditions: pd.Series
    ) -> pd.Series:

        if not conditions:
            raise ValueError(
                "At least one condition is required"
            )

        result = conditions[0].copy()

        for condition in conditions[1:]:

            result = (
                result
                & condition
            )

        return (
            result
            .astype(bool)
            .astype(object)
        )

    @staticmethod
    def any_condition(
        *conditions: pd.Series
    ) -> pd.Series:

        if not conditions:
            raise ValueError(
                "At least one condition is required"
            )

        result = conditions[0].copy()

        for condition in conditions[1:]:

            result = (
                result
                | condition
            )

        return (
            result
            .astype(bool)
            .astype(object)
        )