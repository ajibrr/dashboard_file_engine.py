import pandas as pd

from data.conditions import ConditionEngine


class StrategyEngine:
    """
    Generic strategy engine.

    Responsibilities:
    - Evaluate configured entry conditions
    - Evaluate configured exit conditions
    - Combine conditions using AND / OR logic
    - Produce entry and exit boolean signals

    ConditionEngine remains responsible for individual conditions.
    """

    def __init__(
        self,
        entry_conditions=None,
        exit_conditions=None,
        entry_mode="all",
        exit_mode="all",
    ):
        self.entry_conditions = entry_conditions or []
        self.exit_conditions = exit_conditions or []

        self.entry_mode = entry_mode
        self.exit_mode = exit_mode

        self._validate_mode(self.entry_mode)
        self._validate_mode(self.exit_mode)

    # ============================================================
    # VALIDATION
    # ============================================================

    @staticmethod
    def _validate_mode(mode):

        if mode not in ("all", "any"):
            raise ValueError(
                "mode must be either 'all' or 'any'"
            )

    # ============================================================
    # CONDITION EVALUATION
    # ============================================================

    @staticmethod
    def _evaluate_condition(dataframe, condition):

        if callable(condition):
            result = condition(dataframe)

        elif isinstance(condition, pd.Series):
            result = condition

        else:
            raise TypeError(
                "Condition must be a callable or pandas Series"
            )

        if not isinstance(result, pd.Series):
            raise TypeError(
                "Condition must return a pandas Series"
            )

        result = result.reindex(dataframe.index)

        return result.fillna(False).astype(bool)

    # ============================================================
    # COMBINE CONDITIONS
    # ============================================================

    @staticmethod
    def _combine_conditions(
        dataframe,
        conditions,
        mode,
    ):

        if not conditions:

            return pd.Series(
                False,
                index=dataframe.index,
                dtype=bool,
            )

        evaluated = [
            StrategyEngine._evaluate_condition(
                dataframe,
                condition,
            )
            for condition in conditions
        ]

        combined = evaluated[0]

        for condition in evaluated[1:]:

            if mode == "all":
                combined = combined & condition

            elif mode == "any":
                combined = combined | condition

        return combined.astype(bool)

    # ============================================================
    # ENTRY SIGNAL
    # ============================================================

    def entry_signal(self, dataframe):

        return self._combine_conditions(
            dataframe,
            self.entry_conditions,
            self.entry_mode,
        )

    # ============================================================
    # EXIT SIGNAL
    # ============================================================

    def exit_signal(self, dataframe):

        return self._combine_conditions(
            dataframe,
            self.exit_conditions,
            self.exit_mode,
        )

    # ============================================================
    # BOTH SIGNALS
    # ============================================================

    def signals(self, dataframe):

        result = dataframe.copy()

        result["entry_signal"] = self.entry_signal(
            dataframe
        )

        result["exit_signal"] = self.exit_signal(
            dataframe
        )

        return result

    # ============================================================
    # SIGNAL SUMMARY
    # ============================================================

    def summary(self, dataframe):

        entry = self.entry_signal(dataframe)
        exit_ = self.exit_signal(dataframe)

        return {
            "total_rows": len(dataframe),
            "entry_signals": int(entry.sum()),
            "exit_signals": int(exit_.sum()),
        }