Anomaly Detector module: uses IsolationForest as a quick-start.

Methods:
- AnomalyDetector().score(X_list) -> array of anomaly scores
- AnomalyDetector().is_anomaly(score, threshold=0.5) -> bool

To train a production model, create a training script that fits on labeled/normal data and writes joblib file to this directory.
