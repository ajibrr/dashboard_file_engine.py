import json
from pathlib import Path


class DashboardDataLoader:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def load(self):
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Dashboard file not found: {self.file_path}"
            )

        with self.file_path.open(
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)

        return data

    def load_nifty_seconds(self):
        data = self.load()

        if "nifty_seconds" not in data:
            raise KeyError(
                "nifty_seconds not found in dashboard JSON"
            )

        return data["nifty_seconds"]

    def load_flow(self):
        data = self.load()

        if "flow" not in data:
            raise KeyError(
                "flow not found in dashboard JSON"
            )

        return data["flow"]