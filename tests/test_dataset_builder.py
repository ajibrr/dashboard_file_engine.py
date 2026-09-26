from data.loader import DashboardDataLoader
from data.timeframe_builder import TimeframeBuilder
from data.dataset_builder import DatasetBuilder


INPUT_FILE = (
    r"C:\Users\Ibrrc\Downloads\NSE"
    r"\NIFTY_20260924_DASHBOARD.json"
)


def load_dataset_builder():

    loader = DashboardDataLoader(
        INPUT_FILE
    )

    seconds = loader.load_nifty_seconds()
    flow = loader.load_flow()

    timeframe_builder = TimeframeBuilder(
        seconds,
        flow
    )

    return DatasetBuilder(
        timeframe_builder,
        flow
    )


def test_dataset_builder_12s():

    builder = load_dataset_builder()

    df = builder.build(
        "12s",
        oi_reference="start"
    )

    assert not df.empty

    required_columns = [
        "open",
        "high",
        "low",
        "close",
        "candle_start",
        "candle_end",
        "ce_oi_change",
        "pe_oi_change",
        "cumulative_ce",
        "cumulative_pe",
    ]

    for column in required_columns:
        assert column in df.columns

    print()
    print("=" * 70)
    print("DATASET: 12s")
    print("=" * 70)

    print(df.head(10))


def test_dataset_builder_1m():

    builder = load_dataset_builder()

    df = builder.build(
        "1min",
        oi_reference="start"
    )

    assert not df.empty

    assert "cumulative_ce" in df.columns
    assert "cumulative_pe" in df.columns

    print()
    print("=" * 70)
    print("DATASET: 1min")
    print("=" * 70)

    print(df.head(10))


def test_dataset_builder_3m():

    builder = load_dataset_builder()

    df = builder.build(
        "3min",
        oi_reference="end"
    )

    assert not df.empty

    assert "cumulative_ce" in df.columns
    assert "cumulative_pe" in df.columns

    print()
    print("=" * 70)
    print("DATASET: 3min")
    print("=" * 70)

    print(df.head(10))


def test_dataset_builder_5m():

    builder = load_dataset_builder()

    df = builder.build(
        "5min",
        oi_reference="end"
    )

    assert not df.empty

    assert "cumulative_ce" in df.columns
    assert "cumulative_pe" in df.columns

    print()
    print("=" * 70)
    print("DATASET: 5min")
    print("=" * 70)

    print(df.head(10))