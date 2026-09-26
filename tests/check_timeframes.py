from data.loader import DashboardDataLoader
from data.timeframe_builder import TimeframeBuilder


INPUT_FILE = (
    r"C:\Users\Ibrrc\Downloads\NSE"
    r"\NIFTY_20260924_DASHBOARD.json"
)


def main():

    print("=" * 70)
    print("NIFTY TIMEFRAME VALIDATION")
    print("=" * 70)

    loader = DashboardDataLoader(
        INPUT_FILE
    )

    seconds = loader.load_nifty_seconds()
    flow = loader.load_flow()

    print()
    print(f"Raw NIFTY records : {len(seconds)}")
    print(f"Raw FLOW records  : {len(flow)}")

    builder = TimeframeBuilder(
        seconds,
        flow
    )

    timeframes = {
        "12s": "12s",
        "1m": "1min",
        "3m": "3min",
        "5m": "5min"
    }

    for name, timeframe in timeframes.items():

        print()
        print("-" * 70)
        print(f"TIMEFRAME: {name}")
        print("-" * 70)

        df = builder.build(timeframe)

        print(
            f"Candles      : {len(df)}"
        )

        print(
            f"First candle : {df.index.min()}"
        )

        print(
            f"Last candle  : {df.index.max()}"
        )

        print()
        print(
            df.head(3)
        )

        print()

        print(
            df.tail(3)
        )


if __name__ == "__main__":
    main()