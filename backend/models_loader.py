import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

binary_model = joblib.load(os.path.join(MODEL_DIR, "binary_model.pkl"))

multiclass_model = joblib.load(
    os.path.join(MODEL_DIR, "multiclass_model.pkl")
)

scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))