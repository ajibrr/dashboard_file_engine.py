import pandas as pd

from data.strategy import StrategyEngine


# ============================================================
# FIXTURE
# ============================================================

def sample_df():

    index = pd.date_range(
        "2026-09-24 09:00:00",
        periods=10,
        freq="min",
    )

    return pd.DataFrame(
        {
            "close": [
                100,
                101,
                102,
                103,
                104,
                103,
                102,
                101,
                100,
                99,
            ],
            "sma_9": [
                90,
                91,
                92,
                93,
                94,
                95,
                96,
                97,
                98,
                99,
            ],
            "sma_44": [
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
            ],
            "rsi_14": [
                60,
                65,
                72,
                75,
                80,
                68,
                65,
                60,
                55,
                50,
            ],
        },
        index=index,
    )


# ============================================================
# BASIC CONDITIONS
# ============================================================

def test_entry_all_conditions():

    df = sample_df()

    strategy = StrategyEngine(
        entry_conditions=[
            lambda x: x["sma_9"] > x["sma_44"],
            lambda x: x["rsi_14"] > 70,
        ],
        entry_mode="all",
    )

    result = strategy.entry_signal(df)

    assert result.iloc[0] is False
    assert result.iloc[2] is False
    assert result.iloc[3] is False

    # sma_9 is still below sma_44
    assert result.sum() == 0


# ============================================================
# ANY CONDITION
# ============================================================

def test_entry_any_condition():

    df = sample_df()

    strategy = StrategyEngine(
        entry_conditions=[
            lambda x: x["sma_9"] > x["sma_44"],
            lambda x: x["rsi_14"] > 70,
        ],
        entry_mode="any",
    )

    result = strategy.entry_signal(df)

    assert result.iloc[2] is True
    assert result.iloc[3] is True

    assert result.sum() == 3


# ============================================================
# EXIT
# ============================================================

def test_exit_signal():

    df = sample_df()

    strategy = StrategyEngine(
        exit_conditions=[
            lambda x: x["rsi_14"] < 70,
        ]
    )

    result = strategy.exit_signal(df)

    assert result.iloc[0] is True
    assert result.iloc[2] is False
    assert result.iloc[5] is True


# ============================================================
# BOTH ENTRY AND EXIT
# ============================================================

def test_signals():

    df = sample_df()

    strategy = StrategyEngine(
        entry_conditions=[
            lambda x: x["rsi_14"] > 70,
        ],
        exit_conditions=[
            lambda x: x["rsi_14"] < 70,
        ],
    )

    result = strategy.signals(df)

    assert "entry_signal" in result.columns
    assert "exit_signal" in result.columns

    assert result["entry_signal"].dtype == bool
    assert result["exit_signal"].dtype == bool


# ============================================================
# SUMMARY
# ============================================================

def test_summary():

    df = sample_df()

    strategy = StrategyEngine(
        entry_conditions=[
            lambda x: x["rsi_14"] > 70,
        ],
        exit_conditions=[
            lambda x: x["rsi_14"] < 70,
        ],
    )

    summary = strategy.summary(df)

    assert summary["total_rows"] == 10
    assert summary["entry_signals"] == 3
    assert summary["exit_signals"] == 7


# ============================================================
# EMPTY CONDITIONS
# ============================================================

def test_empty_conditions():

    df = sample_df()

    strategy = StrategyEngine()

    entry = strategy.entry_signal(df)
    exit_ = strategy.exit_signal(df)

    assert len(entry) == len(df)
    assert len(exit_) == len(df)

    assert entry.sum() == 0
    assert exit_.sum() == 0


# ============================================================
# INVALID MODE
# ============================================================

def test_invalid_mode():

    try:

        StrategyEngine(
            entry_mode="invalid"
        )

        assert False

    except ValueError:

        assert True