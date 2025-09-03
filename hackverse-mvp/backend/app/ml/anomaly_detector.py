import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / 'models'
MODEL_PATH.mkdir(exist_ok=True)

class AnomalyDetector:
    def __init__(self):
        # small demonstration model; in prod load a trained model
        self.model_file = MODEL_PATH / 'iso_forest.joblib'
        if self.model_file.exists():
            self.model = joblib.load(self.model_file)
        else:
            self.model = IsolationForest(n_estimators=50, contamination=0.01, random_state=42)
            # fit to random data as placeholder
            X = np.random.randn(1000, 4)
            self.model.fit(X)
            joblib.dump(self.model, self.model_file)

    def score(self, X):
        # return anomaly scores (negative scores from sklearn)
        Xarr = np.array(X)
        return self.model.decision_function(Xarr) * -1.0

    def is_anomaly(self, score, threshold=0.5):
        return score > threshold
