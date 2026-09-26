import pandas as pd


class TimeframeBuilder:

    def __init__(self, price_df, flow_df):
        self.price_df = price_df
        self.flow_df = flow_df

    def build_price_timeframe(self, timeframe):

        df = self.price_df.copy()

        candles = df["nifty"].resample(timeframe).agg(
            open="first",
            high="max",
            low="min",
            close="last"
        )

        candles = candles.dropna()

        return candles

    def build_oi_timeframe(self, timeframe):

        df = self.flow_df.copy()

        oi = df[
            [
                "ce_oi_change",
                "pe_oi_change",
                "cumulative_ce",
                "cumulative_pe"
            ]
        ].resample(timeframe).last()

        oi = oi.ffill()

        return oi

    def build(self, timeframe):

        price = self.build_price_timeframe(timeframe)
        oi = self.build_oi_timeframe(timeframe)

        result = price.join(
            oi,
            how="left"
        )

        result = result.ffill()

        return result