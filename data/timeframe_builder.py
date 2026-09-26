import pandas as pd


class TimeframeBuilder:

    def __init__(self, nifty_seconds, flow):

        self.nifty_seconds = self._prepare_seconds(
            nifty_seconds
        )

        self.flow = self._prepare_flow(
            flow
        )

    # ============================================================
    # PREPARE NIFTY SECOND DATA
    # ============================================================

    @staticmethod
    def _prepare_seconds(records):

        df = pd.DataFrame(records)

        if df.empty:
            raise ValueError(
                "nifty_seconds contains no data"
            )

        required_columns = [
            "timestamp",
            "nifty"
        ]

        missing = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing seconds columns: {missing}"
            )

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        df["nifty"] = pd.to_numeric(
            df["nifty"],
            errors="coerce"
        )

        df = df.dropna(
            subset=[
                "timestamp",
                "nifty"
            ]
        )

        df = df.sort_values(
            "timestamp"
        )

        df = df.drop_duplicates(
            subset=["timestamp"]
        )

        df = df.set_index(
            "timestamp"
        )

        return df

    # ============================================================
    # PREPARE OI FLOW DATA
    #
    # IMPORTANT:
    # OI stays at its original 1-minute frequency.
    #
    # We DO NOT resample OI here.
    # OIMapper is responsible for mapping OI
    # to the strategy timeframe.
    # ============================================================

    @staticmethod
    def _prepare_flow(records):

        df = pd.DataFrame(records)

        if df.empty:
            raise ValueError(
                "flow contains no data"
            )

        required_columns = [
            "timestamp",
            "ce_oi_change",
            "pe_oi_change",
            "cumulative_ce",
            "cumulative_pe"
        ]

        missing = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing flow columns: {missing}"
            )

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        numeric_columns = [
            "ce_oi_change",
            "pe_oi_change",
            "cumulative_ce",
            "cumulative_pe"
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        df = df.dropna(
            subset=[
                "timestamp"
            ]
        )

        df = df.sort_values(
            "timestamp"
        )

        df = df.drop_duplicates(
            subset=["timestamp"]
        )

        df = df.set_index(
            "timestamp"
        )

        return df

    # ============================================================
    # BUILD PRICE CANDLES
    #
    # Supported examples:
    #
    #     12s
    #     1min
    #     3min
    #     5min
    #
    # This method builds PRICE candles only.
    # ============================================================

    def build_price_timeframe(
        self,
        timeframe
    ) -> pd.DataFrame:

        candles = (
            self.nifty_seconds[
                ["nifty"]
            ]
            .resample(
                timeframe,
                label="left",
                closed="left"
            )
            .agg(
                open=("nifty", "first"),
                high=("nifty", "max"),
                low=("nifty", "min"),
                close=("nifty", "last")
            )
        )

        # Remove empty candles
        candles = candles.dropna(
            subset=[
                "open",
                "high",
                "low",
                "close"
            ]
        )

        # --------------------------------------------------------
        # Calculate candle boundaries
        # --------------------------------------------------------

        offset = (
            pd.tseries.frequencies.to_offset(
                timeframe
            )
        )

        candles["candle_start"] = candles.index

        candles["candle_end"] = (
            candles["candle_start"] + offset
        )

        return candles

    # ============================================================
    # BUILD
    #
    # TimeframeBuilder is responsible only for
    # building price candles.
    #
    # OI mapping is handled separately by OIMapper.
    # ============================================================

    def build(
        self,
        timeframe
    ) -> pd.DataFrame:

        return self.build_price_timeframe(
            timeframe
        )