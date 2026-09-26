from indicators.sma import SMA
from indicators.rsi import calculate_rsi


class IndicatorEngine:

    def __init__(
        self,
        sma_periods=None,
        rsi_period=14
    ):

        self.sma_periods = (
            sma_periods
            or [9, 44, 200]
        )

        self.rsi_period = rsi_period

    def calculate(self, df):

        df = df.copy()

        for period in self.sma_periods:

            column = f"sma_{period}"

            df[column] = SMA.calculate(
                df["close"],
                period
            )

        df[
            f"rsi_{self.rsi_period}"
        ] = calculate_rsi(
            df["close"],
            self.rsi_period
        )

        return df