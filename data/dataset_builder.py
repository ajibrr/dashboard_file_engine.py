import pandas as pd

from data.timeframe_builder import TimeframeBuilder
from data.oi_mapper import OIMapper


class DatasetBuilder:

    def __init__(
        self,
        timeframe_builder: TimeframeBuilder,
        flow
    ):

        self.timeframe_builder = timeframe_builder

        self.flow_df = (
            pd.DataFrame(flow)
            .assign(
                timestamp=lambda x:
                pd.to_datetime(x["timestamp"])
            )
            .set_index("timestamp")
        )

        self.oi_mapper = OIMapper(
            self.flow_df
        )

    # ============================================================
    # BUILD DATASET
    # ============================================================

    def build(
        self,
        timeframe: str,
        oi_reference: str = "start"
    ) -> pd.DataFrame:

        # --------------------------------------------------------
        # Build price candles
        # --------------------------------------------------------

        candles = (
            self.timeframe_builder
            .build(timeframe)
        )

        # --------------------------------------------------------
        # Map native 1-minute OI
        # --------------------------------------------------------

        result = self.oi_mapper.map_to_candles(
            candles,
            reference=oi_reference
        )

        return result