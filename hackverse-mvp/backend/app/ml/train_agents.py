"""
Train agent-specific models (EDR and Anomaly) and save them to backend/app/ml/models/
"""
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

MODELS_DIR = Path(__file__).parent / 'models'
MODELS_DIR.mkdir(exist_ok=True)

EDR_MODEL = MODELS_DIR / 'edr_iso.joblib'
ANOM_MODEL = MODELS_DIR / 'iso_forest.joblib'


def generate_synthetic(n_samples=3000, n_features=6, seed=42):
    rng = np.random.RandomState(seed)
    X = rng.normal(loc=0.0, scale=1.0, size=(n_samples, n_features))
    # inject some anomalies
    n_anom = max(10, int(0.01 * n_samples))
    idx = rng.choice(n_samples, n_anom, replace=False)
    X[idx] += rng.normal(8, 2, size=(n_anom, n_features))
    return X


def train_and_save(path, X, n_estimators=100, contamination=0.01):
    print(f"Training IsolationForest -> {path} shape={X.shape}")
    model = IsolationForest(n_estimators=n_estimators, contamination=contamination, random_state=42)
    model.fit(X)
    joblib.dump(model, path)
    print(f"Saved model: {path}")


def main():
    # EDR model trained on 6-dim endpoint telemetry
    X_edr = generate_synthetic(n_samples=2500, n_features=6, seed=1)
    train_and_save(EDR_MODEL, X_edr, n_estimators=100, contamination=0.02)

    # Anomaly model trained on 4-dim logs/features
    X_anom = generate_synthetic(n_samples=2000, n_features=4, seed=2)
    train_and_save(ANOM_MODEL, X_anom, n_estimators=100, contamination=0.01)

if __name__ == '__main__':
    main()
