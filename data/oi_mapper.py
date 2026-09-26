import pandas as pd


class OIMapper:

    OI_COLUMNS = [
        "ce_oi_change",
        "pe_oi_change",
        "cumulative_ce",
        "cumulative_pe",
    ]

    def __init__(self, flow_df):
        """
        Initialize the OI mapper.

        flow_df must contain the native 1-minute OI data.

        Expected index:
            DatetimeIndex

        Expected columns:
            ce_oi_change
            pe_oi_change
            cumulative_ce
            cumulative_pe
        """

        self.flow_df = flow_df.copy()

        # --------------------------------------------------------
        # Validate index
        # --------------------------------------------------------

        if not isinstance(
            self.flow_df.index,
            pd.DatetimeIndex
        ):
            raise ValueError(
                "flow_df must have a DatetimeIndex"
            )

        # --------------------------------------------------------
        # Validate required columns
        # --------------------------------------------------------

        missing = [
            column
            for column in self.OI_COLUMNS
            if column not in self.flow_df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing OI columns: {missing}"
            )

        # --------------------------------------------------------
        # Sort by timestamp
        # --------------------------------------------------------

        self.flow_df = self.flow_df.sort_index()

    # ============================================================
    # GET ORIGINAL 1-MINUTE OI
    # ============================================================

    def get_1m_oi(self):
        """
        Return the original 1-minute OI dataset.

        No resampling.
        No interpolation.
        No forward filling.
        """

        return self.flow_df.copy()

    # ============================================================
    # MAP OI TO STRATEGY CANDLES
    # ============================================================

    def map_to_candles(
        self,
        candle_df,
        reference="start"
    ):
        """
        Map native 1-minute OI values to strategy candles.

        Parameters
        ----------
        candle_df : pandas.DataFrame

            Strategy timeframe candles.

            Must contain:

                candle_start
                candle_end

        reference : str

            "start"
                Use candle_start to determine
                the 1-minute OI reference.

            "end"
                Use candle_end to determine
                the 1-minute OI reference.

        Returns
        -------
        pandas.DataFrame

            Original candle dataframe with
            OI columns attached.
        """

        result = candle_df.copy()

        # --------------------------------------------------------
        # Validate candle index
        # --------------------------------------------------------

        if not isinstance(
            result.index,
            pd.DatetimeIndex
        ):
            raise ValueError(
                "candle_df must have a DatetimeIndex"
            )

        # --------------------------------------------------------
        # Validate reference
        # --------------------------------------------------------

        if reference not in {
            "start",
            "end"
        }:
            raise ValueError(
                "reference must be 'start' or 'end'"
            )

        # --------------------------------------------------------
        # Validate candle boundaries
        # --------------------------------------------------------

        required_boundary_columns = [
            "candle_start",
            "candle_end",
        ]

        missing_boundaries = [
            column
            for column in required_boundary_columns
            if column not in result.columns
        ]

        if missing_boundaries:
            raise ValueError(
                "Missing candle boundary columns: "
                f"{missing_boundaries}"
            )

        # --------------------------------------------------------
        # Determine OI lookup timestamp
        # --------------------------------------------------------

        if reference == "start":

            lookup_times = (
                result["candle_start"]
                .dt.floor("1min")
            )

        else:

            lookup_times = (
                result["candle_end"]
                .dt.floor("1min")
            )

        # --------------------------------------------------------
        # Lookup native 1-minute OI
        # --------------------------------------------------------

        oi = self.flow_df[
            self.OI_COLUMNS
        ].reindex(
            lookup_times
        )

        # --------------------------------------------------------
        # Restore strategy candle index
        # --------------------------------------------------------

        oi.index = result.index

        # --------------------------------------------------------
        # Attach OI columns
        # --------------------------------------------------------

        for column in self.OI_COLUMNS:

            result[column] = oi[column]

        return result