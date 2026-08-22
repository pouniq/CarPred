import os
import logging
from pathlib import Path

import pandas as pd
import numpy as np
from dotenv import load_dotenv
from joblib import load

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "model_dir" / "Linear_Model.joblib"
LOG_PATH = PROJECT_ROOT / os.getenv("LOG_DIR", "logs")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # terminal
        logging.FileHandler(LOG_PATH)  # file
    ],
)


logging.info('loading the trained model ...')
model = load(MODEL_PATH)
logging.info('model loaded.')


def predict(input_data: dict):
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    return prediction



