from data.loader import DashboardDataLoader
from data.timeframe_builder import TimeframeBuilder
from data.dataset_builder import DatasetBuilder

from indicators.indicator_engine import IndicatorEngine


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


def test_indicators_12s():

    builder = load_dataset_builder()

    df = builder.build(
        "12s",
        oi_reference="start"
    )

    engine = IndicatorEngine(
        sma_periods=[9, 44, 200],
        rsi_period=14
    )

    result = engine.calculate(df)

    required_columns = [
        "sma_9",
        "sma_44",
        "sma_200",
        "rsi_14",
    ]

    for column in required_columns:
        assert column in result.columns

    assert len(result) == len(df)

    print()
    print("=" * 70)
    print("INDICATORS: 12s")
    print("=" * 70)

    print(
        result[
            [
                "close",
                "sma_9",
                "sma_44",
                "sma_200",
                "rsi_14",
                "cumulative_ce",
                "cumulative_pe",
            ]
        ].tail(10)
    )


def test_indicators_1m():

    builder = load_dataset_builder()

    df = builder.build(
        "1min",
        oi_reference="start"
    )

    engine = IndicatorEngine(
        sma_periods=[9, 44, 200],
        rsi_period=14
    )

    result = engine.calculate(df)

    required_columns = [
        "sma_9",
        "sma_44",
        "sma_200",
        "rsi_14",
    ]

    for column in required_columns:
        assert column in result.columns

    assert len(result) == len(df)

    print()
    print("=" * 70)
    print("INDICATORS: 1min")
    print("=" * 70)

    print(
        result[
            [
                "close",
                "sma_9",
                "sma_44",
                "sma_200",
                "rsi_14",
                "cumulative_ce",
                "cumulative_pe",
            ]
        ].tail(10)
    )


def test_indicators_3m():

    builder = load_dataset_builder()

    df = builder.build(
        "3min",
        oi_reference="end"
    )

    engine = IndicatorEngine(
        sma_periods=[9, 44, 200],
        rsi_period=14
    )

    result = engine.calculate(df)

    required_columns = [
        "sma_9",
        "sma_44",
        "sma_200",
        "rsi_14",
    ]

    for column in required_columns:
        assert column in result.columns

    assert len(result) == len(df)

    print()
    print("=" * 70)
    print("INDICATORS: 3min")
    print("=" * 70)

    print(
        result[
            [
                "close",
                "sma_9",
                "sma_44",
                "sma_200",
                "rsi_14",
                "cumulative_ce",
                "cumulative_pe",
            ]
        ].tail(10)
    )


def test_indicators_5m():

    builder = load_dataset_builder()

    df = builder.build(
        "5min",
        oi_reference="end"
    )

    engine = IndicatorEngine(
        sma_periods=[9, 44, 200],
        rsi_period=14
    )

    result = engine.calculate(df)

    required_columns = [
        "sma_9",
        "sma_44",
        "sma_200",
        "rsi_14",
    ]

    for column in required_columns:
        assert column in result.columns

    assert len(result) == len(df)

    print()
    print("=" * 70)
    print("INDICATORS: 5min")
    print("=" * 70)

    print(
        result[
            [
                "close",
                "sma_9",
                "sma_44",
                "sma_200",
                "rsi_14",
                "cumulative_ce",
                "cumulative_pe",
            ]
        ].tail(10)
    )