"""4-state Hidden Markov Model for market regime detection."""
import numpy as np
from hmmlearn import hmm
import joblib
from loguru import logger
from sklearn.preprocessing import StandardScaler

class RegimeDetector:
    REGIME_NAMES = ['Bull Trend', 'Bear Trend', 'Ranging', 'High Volatility']

    def __init__(self, n_regimes: int = 4):
        self.n_regimes = n_regimes
        self.model = hmm.GaussianHMM(
            n_components=n_regimes,
            covariance_type='full',
            n_iter=1000,
            random_state=42
        )
        self.scaler = StandardScaler()

    def fit(self, returns: np.ndarray, volumes: np.ndarray) -> None:
        X = np.column_stack([returns, volumes, returns**2, np.abs(returns)])
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        logger.success('HMM trained successfully')

    def predict(self, returns: np.ndarray, volumes: np.ndarray) -> tuple[int, str, np.ndarray]:
        X = np.column_stack([returns, volumes, returns**2, np.abs(returns)])
        if hasattr(self.scaler, 'mean_'):
            X = self.scaler.transform(X)
        states = self.model.predict(X)
        probs = self.model.predict_proba(X)
        current = int(states[-1])
        return current, self.REGIME_NAMES[current], probs[-1]

    def save(self, path: str = 'models/hmm.pkl') -> None:
        joblib.dump(self.model, path)
        logger.info(f'Saved HMM to {path}')

    def load(self, path: str = 'models/hmm.pkl') -> None:
        self.model = joblib.load(path)
        logger.info(f'Loaded HMM from {path}')
