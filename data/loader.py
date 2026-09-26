import json
import pandas as pd


class NiftyDataLoader:

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def load_seconds(self):
        data = self.load()

        df = pd.DataFrame(data["nifty_seconds"])

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        df = df.sort_values("timestamp")
        df = df.drop_duplicates("timestamp")

        df = df.set_index("timestamp")

        return df

    def load_flow(self):
        data = self.load()

        df = pd.DataFrame(data["flow"])

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        df = df.sort_values("timestamp")
        df = df.drop_duplicates("timestamp")

        df = df.set_index("timestamp")

        return df