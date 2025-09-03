"""
Train and save an IsolationForest model for the HACKVERSE MVP.

Usage:
  - Use default synthetic data for a quick train:
      python train_model.py
  - Train from a CSV file (rows=observations, cols=features):
      python train_model.py --input data.csv --output iso_forest.joblib --n-estimators 100 --contamination 0.01

The trained model is saved into the `backend/app/ml/models/` directory as `iso_forest.joblib` by default.
"""
from pathlib import Path
import argparse
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

MODELS_DIR = Path(__file__).parent / 'models'
MODELS_DIR.mkdir(exist_ok=True)

DEFAULT_MODEL = MODELS_DIR / 'iso_forest.joblib'


def load_csv(path: Path):
    import csv
    rows = []
    with path.open('r', newline='') as f:
        reader = csv.reader(f)
        for r in reader:
            if not r:
                continue
            rows.append([float(x) for x in r])
    return np.array(rows)


def generate_synthetic(n_samples=2000, n_features=4):
    # generate mostly normal data with small random variation
    rng = np.random.RandomState(42)
    X = rng.normal(loc=0.0, scale=1.0, size=(n_samples, n_features))
    return X


def train_and_save(X, n_estimators=100, contamination=0.01, output_path=DEFAULT_MODEL):
    print(f"Training IsolationForest (n_estimators={n_estimators}, contamination={contamination}) on data shape {X.shape}")
    model = IsolationForest(n_estimators=n_estimators, contamination=contamination, random_state=42)
    model.fit(X)
    joblib.dump(model, output_path)
    print(f"Saved model to {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, help='CSV file with numeric features')
    parser.add_argument('--output', '-o', type=str, default=str(DEFAULT_MODEL), help='Output joblib path')
    parser.add_argument('--n-estimators', type=int, default=100)
    parser.add_argument('--contamination', type=float, default=0.01)
    parser.add_argument('--samples', type=int, default=2000)
    parser.add_argument('--features', type=int, default=4)
    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            raise SystemExit(f"Input file not found: {input_path}")
        X = load_csv(input_path)
    else:
        X = generate_synthetic(n_samples=args.samples, n_features=args.features)

    out = Path(args.output)
    train_and_save(X, n_estimators=args.n_estimators, contamination=args.contamination, output_path=out)


if __name__ == '__main__':
    main()
