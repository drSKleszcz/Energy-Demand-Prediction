import xgboost as xgb
from pipline import EnergyDataPipeline

# Load the model
model = xgb.XGBRegressor()
model.load_model("models//xboost_test.json")


pipeline = EnergyDataPipeline()
pipeline.load_data()
pipeline.preprocess()
pipeline.add_time_features()
pipeline.add_lag_features()

df_final = pipeline.get_processed_data()
df_final = df_final.fillna(0)
df_final = df_final.drop(columns=["load_MW"])



X = df_final

predictions = model.predict(X)
df_final["forecast"] = predictions
df_final[["forecast"]].to_sql("forecast_output", con=pipeline.engine, if_exists="replace")
print(df_final)