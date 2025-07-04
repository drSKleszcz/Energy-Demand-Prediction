import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from zoneinfo import ZoneInfo


class EnergyDataPipeline:
    def __init__(self, db_path="sqlite:///database//entsoe_load.db"):
        self.engine = create_engine(db_path)
        self.df = None


    def load_data(self, table_name="load_data"):
        """Load data from the database into a DataFrame"""
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM {table_name}")
            self.df = pd.read_sql(query, conn, parse_dates=["timestamp"])
        
        self.df.set_index("timestamp", inplace=True)
        self.df.sort_index(inplace=True)
        return self.df


    def preprocess(self):
        """Convert timezones and drop duplicates/nulls"""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Ensure UTC, convert to Warsaw, remove tz
        self.df.index = self.df.index.tz_localize("UTC").tz_convert("Europe/Warsaw").tz_localize(None)

        # Drop duplicates and missing
        self.df = self.df[~self.df.index.duplicated(keep='last')]
        self.df = self.df.dropna()

        return self.df
    

    def _is_daytime(self, ts):
        """Classify time as 'day' or 'night' based on sunrise/sunset (Warsaw)"""
        from astral import LocationInfo
        from astral.sun import sun

        loc = LocationInfo("Warsaw", "Poland", "Europe/Warsaw", 52.23, 21.01)
        local_time = ts.replace(tzinfo=ZoneInfo("Europe/Warsaw"))
        s = sun(loc.observer, date=local_time.date(), tzinfo=loc.timezone)

        return 1 if s["sunrise"] <= local_time <= s["sunset"] else 0
    

    def add_time_features(self):
        """Add time-based features like hour, day_of_week, is_weekend, day_night"""
        if self.df is None:
            raise ValueError("Data not loaded.")

        self.df["hour"] = self.df.index.hour
        self.df["day_night"] = self.df.index.to_series().apply(self._is_daytime)
        return self.df
    
    
    def add_lag_features(self):
        """Add lag features like 1h, 2h, and 24h previous load"""
        if self.df is None or "load_MW" not in self.df.columns:
            raise ValueError("Data must be loaded and include 'load_MW' column.")

        self.df["Load_lag_1h"] = self.df["load_MW"].shift(1)
        self.df["Load_lag_2h"] = self.df["load_MW"].shift(2)
        self.df["Load_lag_24h"] = self.df["load_MW"].shift(24)

        return self.df
    
    def drop_load(self):
        self.df = self.df.drop(["load_MW"])
        return self.df   


    def get_processed_data(self):
        """Return the final processed DataFrame"""
        return self.df
    

    


pipeline = EnergyDataPipeline()
pipeline.load_data()
pipeline.preprocess()
pipeline.add_time_features()
pipeline.add_lag_features()

df_final = pipeline.get_processed_data()
df_final = df_final.fillna(0)
print(df_final)