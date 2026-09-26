from data.loader import DashboardDataLoader
from data.timeframe_builder import TimeframeBuilder


INPUT_FILE = (
    r"C:\Users\Ibrrc\Downloads\NSE"
    r"\NIFTY_20260924_DASHBOARD.json"
)


def test_timeframe_builder():

    loader = DashboardDataLoader(
        INPUT_FILE
    )

    seconds = loader.load_nifty_seconds()
    flow = loader.load_flow()

    builder = TimeframeBuilder(
        seconds,
        flow
    )

    # --------------------------------------------------------
    # Test 1-minute candles
    # --------------------------------------------------------

    df_1m = builder.build("1min")

    assert not df_1m.empty

    required_columns = [
        "open",
        "high",
        "low",
        "close",
        "candle_start",
        "candle_end"
    ]

    for column in required_columns:

        assert column in df_1m.columns

    # --------------------------------------------------------
    # Verify candle boundaries
    # --------------------------------------------------------

    first_candle = df_1m.iloc[0]

    assert (
        first_candle["candle_end"]
        > first_candle["candle_start"]
    )

    # --------------------------------------------------------
    # Print information
    # --------------------------------------------------------

    print()
    print("TIMEFRAME: 1min")
    print("-" * 60)

    print(
        "Candles      :",
        len(df_1m)
    )

    print(
        "First candle :",
        df_1m["candle_start"].iloc[0]
    )

    print(
        "Last candle  :",
        df_1m["candle_start"].iloc[-1]
    )

    print()

    print(
        df_1m.head(5)
    )