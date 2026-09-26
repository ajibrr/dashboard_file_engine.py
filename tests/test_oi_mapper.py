import pandas as pd

from data.loader import DashboardDataLoader
from data.timeframe_builder import TimeframeBuilder
from data.oi_mapper import OIMapper


INPUT_FILE = (
    r"C:\Users\Ibrrc\Downloads\NSE"
    r"\NIFTY_20260924_DASHBOARD.json"
)


def load_engine():

    loader = DashboardDataLoader(
        INPUT_FILE
    )

    seconds = loader.load_nifty_seconds()
    flow = loader.load_flow()

    builder = TimeframeBuilder(
        seconds,
        flow
    )

    return builder, flow


# ============================================================
# 12 SECOND OI MAPPING
# ============================================================

def test_oi_mapper_12s():

    builder, flow = load_engine()

    candles = builder.build("12s")

    mapper = OIMapper(
        pd.DataFrame(flow)
        .assign(
            timestamp=lambda x:
            pd.to_datetime(x["timestamp"])
        )
        .set_index("timestamp")
    )

    result = mapper.map_to_candles(
        candles,
        reference="start"
    )

    # --------------------------------------------------------
    # Candle boundaries must not change
    # --------------------------------------------------------

    assert (
        result.iloc[0]["candle_start"]
        == candles.iloc[0]["candle_start"]
    )

    assert (
        result.iloc[0]["candle_end"]
        == candles.iloc[0]["candle_end"]
    )

    # --------------------------------------------------------
    # OI columns must exist
    # --------------------------------------------------------

    assert "cumulative_ce" in result.columns
    assert "cumulative_pe" in result.columns

    # --------------------------------------------------------
    # Print
    # --------------------------------------------------------

    print()
    print("12s OI mapping:")
    print(
        result[
            [
                "close",
                "cumulative_ce",
                "cumulative_pe"
            ]
        ].head(10)
    )


# ============================================================
# 1 MINUTE OI MAPPING
# ============================================================

def test_oi_mapper_1m():

    builder, flow = load_engine()

    candles = builder.build("1min")

    mapper = OIMapper(
        pd.DataFrame(flow)
        .assign(
            timestamp=lambda x:
            pd.to_datetime(x["timestamp"])
        )
        .set_index("timestamp")
    )

    result = mapper.map_to_candles(
        candles,
        reference="start"
    )

    # --------------------------------------------------------
    # OI columns
    # --------------------------------------------------------

    assert "cumulative_ce" in result.columns
    assert "cumulative_pe" in result.columns

    # --------------------------------------------------------
    # Print
    # --------------------------------------------------------

    print()
    print("1m OI mapping:")
    print(
        result[
            [
                "close",
                "cumulative_ce",
                "cumulative_pe"
            ]
        ].head(10)
    )


# ============================================================
# 5 MINUTE OI MAPPING
#
# IMPORTANT:
#
# 5-minute candle:
#
#     09:15 → 09:20
#
# uses OI at:
#
#     09:20
#
# Therefore reference="end".
# ============================================================

def test_oi_mapper_5m_end():

    builder, flow = load_engine()

    candles = builder.build("5min")

    mapper = OIMapper(
        pd.DataFrame(flow)
        .assign(
            timestamp=lambda x:
            pd.to_datetime(x["timestamp"])
        )
        .set_index("timestamp")
    )

    result = mapper.map_to_candles(
        candles,
        reference="end"
    )

    # --------------------------------------------------------
    # OI columns
    # --------------------------------------------------------

    assert "cumulative_ce" in result.columns
    assert "cumulative_pe" in result.columns

    # --------------------------------------------------------
    # Print
    # --------------------------------------------------------

    print()
    print("5m END OI mapping:")
    print(
        result[
            [
                "close",
                "cumulative_ce",
                "cumulative_pe"
            ]
        ].head(10)
    )