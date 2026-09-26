import pandas as pd
import pytest

from data.conditions import ConditionEngine


@pytest.fixture
def sample_df():

    index = pd.date_range(
        "2026-09-24 09:00:00",
        periods=10,
        freq="1min"
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
                99
            ],

            "sma_9": [
                100,
                101,
                102,
                103,
                104,
                105,
                106,
                107,
                108,
                109
            ],

            "sma_44": [
                110,
                110,
                110,
                110,
                110,
                104,
                104,
                104,
                104,
                104
            ],

            "sma_200": [
                120,
                120,
                120,
                120,
                120,
                120,
                120,
                120,
                120,
                120
            ],

            "rsi_14": [
                50,
                55,
                60,
                65,
                71,
                75,
                68,
                60,
                55,
                50
            ],

            "cumulative_ce": [
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190
            ],

            "cumulative_pe": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110
            ],
        },
        index=index
    )


# ============================================================
# SIMPLE COMPARISON TESTS
# ============================================================


def test_greater_than(sample_df):

    result = ConditionEngine.greater_than(
        sample_df,
        "rsi_14",
        70
    )

    assert result.iloc[4] is True
    assert result.iloc[0] is False


def test_less_than(sample_df):

    result = ConditionEngine.less_than(
        sample_df,
        "rsi_14",
        70
    )

    assert result.iloc[0] is True
    assert result.iloc[4] is False


# ============================================================
# COLUMN VS COLUMN
# ============================================================


def test_column_greater_than(sample_df):

    result = ConditionEngine.column_greater_than(
        sample_df,
        "sma_9",
        "sma_44"
    )

    assert result.iloc[5] is True
    assert result.iloc[0] is False


def test_column_less_than(sample_df):

    result = ConditionEngine.column_less_than(
        sample_df,
        "sma_9",
        "sma_200"
    )

    assert result.all()


# ============================================================
# RISING
# ============================================================


def test_rising_one_candle(sample_df):

    result = ConditionEngine.rising(
        sample_df,
        "sma_9",
        candles=1
    )

    assert result.iloc[0] is False
    assert result.iloc[1] is True
    assert result.iloc[9] is True


def test_rising_three_candles(sample_df):

    result = ConditionEngine.rising(
        sample_df,
        "sma_9",
        candles=3
    )

    assert result.iloc[0] is False
    assert result.iloc[1] is False
    assert result.iloc[2] is False
    assert result.iloc[3] is True
    assert result.iloc[9] is True


# ============================================================
# FALLING
# ============================================================


def test_falling_one_candle(sample_df):

    result = ConditionEngine.falling(
        sample_df,
        "cumulative_pe",
        candles=1
    )

    assert result.iloc[0] is False
    assert result.iloc[1] is True
    assert result.iloc[9] is True


def test_falling_three_candles(sample_df):

    result = ConditionEngine.falling(
        sample_df,
        "cumulative_pe",
        candles=3
    )

    assert result.iloc[0] is False
    assert result.iloc[1] is False
    assert result.iloc[2] is False
    assert result.iloc[3] is True


# ============================================================
# LOOKBACK
# ============================================================


def test_greater_than_lookback(sample_df):

    result = ConditionEngine.greater_than_lookback(
        sample_df,
        "sma_9",
        lookback=3
    )

    assert result.iloc[0] is False
    assert result.iloc[3] is True
    assert result.iloc[9] is True


def test_less_than_lookback(sample_df):

    result = ConditionEngine.less_than_lookback(
        sample_df,
        "sma_200",
        lookback=3
    )

    assert result.iloc[0] is False
    assert result.iloc[3] is False


# ============================================================
# GREATER THAN ALL PREVIOUS
# ============================================================


def test_greater_than_all_previous(sample_df):

    result = ConditionEngine.greater_than_all_previous(
        sample_df,
        "cumulative_ce",
        lookback=3
    )

    assert result.iloc[0] is False
    assert result.iloc[1] is False
    assert result.iloc[2] is False
    assert result.iloc[3] is True
    assert result.iloc[9] is True


# ============================================================
# LESS THAN ALL PREVIOUS
# ============================================================


def test_less_than_all_previous(sample_df):

    result = ConditionEngine.less_than_all_previous(
        sample_df,
        "cumulative_pe",
        lookback=3
    )

    assert result.iloc[0] is False
    assert result.iloc[1] is False
    assert result.iloc[2] is False
    assert result.iloc[3] is True
    assert result.iloc[9] is True


# ============================================================
# RSI
# ============================================================


def test_rsi_above(sample_df):

    result = ConditionEngine.rsi_above(
        sample_df,
        "rsi_14",
        70
    )

    assert result.iloc[3] is False
    assert result.iloc[4] is True
    assert result.iloc[5] is True


def test_rsi_below(sample_df):

    result = ConditionEngine.rsi_below(
        sample_df,
        "rsi_14",
        70
    )

    assert result.iloc[0] is True
    assert result.iloc[4] is False


# ============================================================
# OI
# ============================================================


def test_oi_increasing(sample_df):

    result = ConditionEngine.oi_increasing(
        sample_df,
        "cumulative_ce"
    )

    assert result.iloc[0] is False
    assert result.iloc[1] is True
    assert result.iloc[9] is True


def test_oi_decreasing(sample_df):

    result = ConditionEngine.oi_decreasing(
        sample_df,
        "cumulative_pe"
    )

    assert result.iloc[0] is False
    assert result.iloc[1] is True
    assert result.iloc[9] is True


# ============================================================
# COMBINE CONDITIONS
# ============================================================


def test_all_conditions(sample_df):

    sma_condition = ConditionEngine.column_greater_than(
        sample_df,
        "sma_9",
        "sma_44"
    )

    rsi_condition = ConditionEngine.rsi_above(
        sample_df,
        "rsi_14",
        70
    )

    combined = ConditionEngine.all_conditions(
        sma_condition,
        rsi_condition
    )
    print()
    print("========== ROW 4 DEBUG ==========")
    print("sma_9  :", sample_df.iloc[4]["sma_9"])
    print("sma_44 :", sample_df.iloc[4]["sma_44"])
    print("rsi_14 :", sample_df.iloc[4]["rsi_14"])
    print("SMA condition :", sma_condition.iloc[4])
    print("RSI condition :", rsi_condition.iloc[4])
    print("COMBINED       :", combined.iloc[4])
    print("=================================")
    assert combined.iloc[4] is False
    assert combined.iloc[5] is True
    assert combined.iloc[0] is False


def test_any_condition(sample_df):

    rsi_condition = ConditionEngine.rsi_above(
        sample_df,
        "rsi_14",
        70
    )

    ce_condition = ConditionEngine.oi_increasing(
        sample_df,
        "cumulative_ce"
    )

    combined = ConditionEngine.any_condition(
        rsi_condition,
        ce_condition
    )

    assert combined.iloc[1] is True
    assert combined.iloc[4] is True