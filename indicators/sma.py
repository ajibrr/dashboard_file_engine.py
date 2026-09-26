import pandas as pd


class SMA:

    @staticmethod
    def calculate(
        series: pd.Series,
        period: int
    ) -> pd.Series:

        if period <= 0:
            raise ValueError(
                "SMA period must be greater than 0"
            )

        return series.rolling(
            window=period,
            min_periods=period
        ).mean()