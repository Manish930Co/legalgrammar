

import os
import tensorflow as tf
from tensorflow.keras.models import load_model


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.h5")


try:
    model = load_model(MODEL_PATH)
    print(f"Loaded model from: {MODEL_PATH}")
except Exception as e:
    print("Error loading model:", e)
    model = None


def predict(text: str):
    """
    prediction function.
    Replace this with your actual preprocessing & prediction logic.
    """
    if model is None:
        return {"error": "Model not loaded"}


    import numpy as np
    dummy_input = np.random.rand(1, 10)


    prediction = model.predict(dummy_input)

    return {
        "input_text": text,
        "raw_prediction": prediction.tolist()
    }

