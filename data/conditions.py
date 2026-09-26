import pandas as pd


class ConditionEngine:
    """
    Generic condition engine for the backtesting framework.

    All condition methods return a pandas Series containing
    native Python bool values rather than numpy.bool_ values.
    This allows tests such as:

        result.iloc[0] is True
        result.iloc[0] is False
    """

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    @staticmethod
    def _validate_column(df, column):
        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' not found in dataframe"
            )

    @staticmethod
    def _validate_lookback(lookback):
        if not isinstance(lookback, int):
            raise TypeError(
                "lookback must be an integer"
            )

        if lookback <= 0:
            raise ValueError(
                "lookback must be greater than 0"
            )

    @staticmethod
    def _bool_series(values, index):
        """
        Convert values into a pandas Series containing
        native Python bool objects.
        """

        return pd.Series(
            [bool(value) for value in values],
            index=index,
            dtype=object
        )

    # ============================================================
    # BASIC COMPARISON
    # ============================================================

    @staticmethod
    def greater_than(df, column, value):

        ConditionEngine._validate_column(
            df,
            column
        )

        return ConditionEngine._bool_series(
            df[column] > value,
            df.index
        )

    @staticmethod
    def less_than(df, column, value):

        ConditionEngine._validate_column(
            df,
            column
        )

        return ConditionEngine._bool_series(
            df[column] < value,
            df.index
        )

    # ============================================================
    # COLUMN VS COLUMN
    # ============================================================

    @staticmethod
    def column_greater_than(
        df,
        column_a,
        column_b
    ):

        ConditionEngine._validate_column(
            df,
            column_a
        )

        ConditionEngine._validate_column(
            df,
            column_b
        )

        return ConditionEngine._bool_series(
            df[column_a] > df[column_b],
            df.index
        )

    @staticmethod
    def column_less_than(
        df,
        column_a,
        column_b
    ):

        ConditionEngine._validate_column(
            df,
            column_a
        )

        ConditionEngine._validate_column(
            df,
            column_b
        )

        return ConditionEngine._bool_series(
            df[column_a] < df[column_b],
            df.index
        )

    # ============================================================
    # RISING CONDITIONS
    # ============================================================

    @staticmethod
    def rising_one_candle(
        df,
        column
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        values = df[column]

        result = (
            values > values.shift(1)
        )

        # First candle has no previous candle.
        result.iloc[0] = False

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    @staticmethod
    def rising_three_candles(
        df,
        column
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        values = df[column]

        result = (
            (values > values.shift(1))
            &
            (values.shift(1) > values.shift(2))
            &
            (values.shift(2) > values.shift(3))
        )

        # First three candles cannot satisfy
        # a three-candle rising condition.
        result.iloc[:3] = False

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    # ============================================================
    # FALLING CONDITIONS
    # ============================================================

    @staticmethod
    def falling_one_candle(
        df,
        column
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        values = df[column]

        result = (
            values < values.shift(1)
        )

        result.iloc[0] = False

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    @staticmethod
    def falling_three_candles(
        df,
        column
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        values = df[column]

        result = (
            (values < values.shift(1))
            &
            (values.shift(1) < values.shift(2))
            &
            (values.shift(2) < values.shift(3))
        )

        result.iloc[:3] = False

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    # ============================================================
    # LOOKBACK COMPARISON
    # ============================================================

    @staticmethod
    def greater_than_lookback(
        df,
        column,
        lookback
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        ConditionEngine._validate_lookback(
            lookback
        )

        values = df[column]

        result = (
            values >
            values.shift(lookback)
        )

        # Not enough historical candles.
        result.iloc[:lookback] = False

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    @staticmethod
    def less_than_lookback(
        df,
        column,
        lookback
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        ConditionEngine._validate_lookback(
            lookback
        )

        values = df[column]

        result = (
            values <
            values.shift(lookback)
        )

        result.iloc[:lookback] = False

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    # ============================================================
    # GREATER THAN ALL PREVIOUS VALUES
    # ============================================================

    @staticmethod
    def greater_than_all_previous(
        df,
        column,
        lookback
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        ConditionEngine._validate_lookback(
            lookback
        )

        values = df[column]

        result = []

        for i in range(len(values)):

            if i < lookback:
                result.append(False)
                continue

            current = values.iloc[i]

            previous = values.iloc[
                i - lookback:i
            ]

            if pd.isna(current):
                result.append(False)
                continue

            if previous.isna().any():
                result.append(False)
                continue

            result.append(
                bool(current > previous.max())
            )

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    # ============================================================
    # LESS THAN ALL PREVIOUS VALUES
    # ============================================================

    @staticmethod
    def less_than_all_previous(
        df,
        column,
        lookback
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        ConditionEngine._validate_lookback(
            lookback
        )

        values = df[column]

        result = []

        for i in range(len(values)):

            if i < lookback:
                result.append(False)
                continue

            current = values.iloc[i]

            previous = values.iloc[
                i - lookback:i
            ]

            if pd.isna(current):
                result.append(False)
                continue

            if previous.isna().any():
                result.append(False)
                continue

            result.append(
                bool(current < previous.min())
            )

        return ConditionEngine._bool_series(
            result,
            df.index
        )
        # ============================================================
    # GENERIC RISING CONDITION
    # ============================================================

    @staticmethod
    def rising(
        df,
        column,
        candles=1
    ):
        """
        Check whether a column has risen for the
        specified number of consecutive candles.

        candles=1:
            current > previous

        candles=3:
            current > previous
            previous > two candles ago
            two candles ago > three candles ago
        """

        ConditionEngine._validate_column(
            df,
            column
        )

        ConditionEngine._validate_lookback(
            candles
        )

        values = df[column]

        result = []

        for i in range(len(values)):

            if i < candles:
                result.append(False)
                continue

            current_is_rising = True

            for step in range(candles):

                current_value = values.iloc[
                    i - step
                ]

                previous_value = values.iloc[
                    i - step - 1
                ]

                if (
                    pd.isna(current_value)
                    or pd.isna(previous_value)
                    or not (
                        current_value > previous_value
                    )
                ):
                    current_is_rising = False
                    break

            result.append(
                current_is_rising
            )

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    # ============================================================
    # GENERIC FALLING CONDITION
    # ============================================================

    @staticmethod
    def falling(
        df,
        column,
        candles=1
    ):
        """
        Check whether a column has fallen for the
        specified number of consecutive candles.

        candles=1:
            current < previous

        candles=3:
            current < previous
            previous < two candles ago
            two candles ago < three candles ago
        """

        ConditionEngine._validate_column(
            df,
            column
        )

        ConditionEngine._validate_lookback(
            candles
        )

        values = df[column]

        result = []

        for i in range(len(values)):

            if i < candles:
                result.append(False)
                continue

            current_is_falling = True

            for step in range(candles):

                current_value = values.iloc[
                    i - step
                ]

                previous_value = values.iloc[
                    i - step - 1
                ]

                if (
                    pd.isna(current_value)
                    or pd.isna(previous_value)
                    or not (
                        current_value < previous_value
                    )
                ):
                    current_is_falling = False
                    break

            result.append(
                current_is_falling
            )

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    # ============================================================
    # RSI CONDITIONS
    # ============================================================

    @staticmethod
    def rsi_above(
        df,
        column,
        value
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        result = df[column] > value

        # NaN RSI must not trigger a condition.
        result = result.where(
            df[column].notna(),
            False
        )

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    @staticmethod
    def rsi_below(
        df,
        column,
        value
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        result = df[column] < value

        result = result.where(
            df[column].notna(),
            False
        )

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    # ============================================================
    # OI CONDITIONS
    # ============================================================

    @staticmethod
    def oi_increasing(
        df,
        column
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        values = df[column]

        result = (
            values > values.shift(1)
        )

        result.iloc[0] = False

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    @staticmethod
    def oi_decreasing(
        df,
        column
    ):

        ConditionEngine._validate_column(
            df,
            column
        )

        values = df[column]

        result = (
            values < values.shift(1)
        )

        result.iloc[0] = False

        return ConditionEngine._bool_series(
            result,
            df.index
        )

    # ============================================================
    # COMBINE ALL CONDITIONS
    # ============================================================

    @staticmethod
    def all_conditions(
        *conditions
    ):

        if not conditions:
            raise ValueError(
                "At least one condition is required"
            )

        first = conditions[0]

        result = pd.Series(
            [True] * len(first),
            index=first.index,
            dtype=object
        )

        for condition in conditions:

            if not isinstance(
                condition,
                pd.Series
            ):
                raise TypeError(
                    "Each condition must be a pandas Series"
                )

            if not condition.index.equals(
                result.index
            ):
                raise ValueError(
                    "All conditions must have "
                    "the same index"
                )

            result = ConditionEngine._bool_series(
                [
                    bool(a) and bool(b)
                    for a, b in zip(
                        result,
                        condition
                    )
                ],
                result.index
            )

        return result

    # ============================================================
    # COMBINE ANY CONDITION
    # ============================================================

    @staticmethod
    def any_condition(
        *conditions
    ):

        if not conditions:
            raise ValueError(
                "At least one condition is required"
            )

        first = conditions[0]

        result = pd.Series(
            [False] * len(first),
            index=first.index,
            dtype=object
        )

        for condition in conditions:

            if not isinstance(
                condition,
                pd.Series
            ):
                raise TypeError(
                    "Each condition must be a pandas Series"
                )

            if not condition.index.equals(
                result.index
            ):
                raise ValueError(
                    "All conditions must have "
                    "the same index"
                )

            result = ConditionEngine._bool_series(
                [
                    bool(a) or bool(b)
                    for a, b in zip(
                        result,
                        condition
                    )
                ],
                result.index
            )

        return result
    